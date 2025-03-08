# # Load data into dataframe
import os
import iris
from sentence_transformers import SentenceTransformer
import pandas as pd
df = pd.read_csv("./Code/IRIS DB/ePROM data.csv")


# Load pretrained Transformer model (we use 'all-MiniLM-L6-v2' lightweight multipurpose, can change later)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for ePROM options, append to dataframe
embeddings = model.encode(df['Options'].tolist(), normalize_embeddings=True)
df['Options_vector'] = embeddings.tolist()


# Connect to database
# Go to Docker and start IRIS instance before running this code section

# Credentials
username = 'demo'
password = 'demo'
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
port = '1972'
namespace = 'USER'

# Concat connection string
CONNECTION_STRING = f"{hostname}:{port}/{namespace}"

# Connect to IRIS
connect = iris.connect(CONNECTION_STRING, username, password)
try:
    cursor = connect.cursor()
except:
    print("Check that IRIS instance is running on Docker")


# Create IRIS table
table_name = "ePROM_DB"
table_definition = "(Question_number VARCHAR(255), Question VARCHAR(255), Options VARCHAR(255), Options_vector VECTOR(DOUBLE, 384))"

# Delete existing table (in case of multiple runs of this block)
try:
    cursor.execute(f"DROP TABLE {table_name}")
    print('Existing table deleted and replaced')
except:
    print('No existing table conflict')
    pass

cursor.execute(f"CREATE TABLE {table_name} {table_definition}")

# Populate database with data from dataframe as a batch using SQL
sql_add_data = f"""
    INSERT INTO {table_name}
    (Question_number, Question, Options, Options_vector)
    VALUES (?, ?, ?, TO_VECTOR(?))
"""
# Prepare list of tuples (parameter for each row)
data = [
    (
        row['Question_number'],
        row['Question'],
        row['Options'],
        str(row['Options_vector'])
    )
    for index, row in df.iterrows()
]

cursor.executemany(sql_add_data, data)


search_phrase = ""  # Insert a string for vector search
search_vector = model.encode(
    # Vectorize search phrase
    search_phrase, normalize_embeddings=True).tolist()

# Define the SQL query with placeholders for the vector and limit, dot product similarity search
sql = f"""
    SELECT TOP ? Question_number, Question, Option,
    FROM {table_name}
    ORDER BY VECTOR_DOT_PRODUCT(Option_vector, TO_VECTOR(?)) DESC
"""
number_of_results = 1
query_vector = search_vector

# Execute SQL query
cursor.execute(sql, [number_of_results, str(query_vector)])

# Fetch results
results = cursor.fetchall()
for i in results:
    print(i)
