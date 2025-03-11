# %% [markdown]
# ## IRIS Database Generator
# - Build IRIS database from .csv
# - Store ePROM data (SQL DB)
# - Vectorize ePROM options (vector DB)

# %% [markdown]
# ### Load ePROM data from csv

# %%
# Load data into dataframe
import os
import iris
from sentence_transformers import SentenceTransformer
import pandas as pd


def setup():
    df = pd.read_csv("./setup/ePROM-data.csv")


# %% [markdown]
# ### Create embeddings from ePROM options using BERT Sentence Transformers

# Load pretrained Transformer model (we use 'all-MiniLM-L6-v2' lightweight multipurpose, can change later)
    model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for ePROM options, append to dataframe
    embeddings = model.encode(
        df['Options'].tolist(), normalize_embeddings=True)
    df['Options_vector'] = embeddings.tolist()

    print("Question Option vectorsization complete.")

# %% [markdown]
# ### IRIS database operations
#
# Management portal: http://localhost:52773/csp/sys/UtilHome.csp

# %%
# Import relevant libraries

# %%
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

# %%
# # Create IRIS tables
    cursor.execute("DROP TABLE IF EXISTS session_history")
    cursor.execute("DROP TABLE IF EXISTS session_qn_ans")
    cursor.execute("DROP TABLE IF EXISTS question_option")
    cursor.execute("DROP TABLE IF EXISTS question")
    cursor.execute("DROP TABLE IF EXISTS session")

    cursor.execute("""
        CREATE TABLE question (
        id INT PRIMARY KEY,
        name varchar(255) NOT NULL,
        description varchar(2047))
    """)

    cursor.execute("""
        CREATE TABLE question_option (
        question_id INT references question (id),
        id INT,
        description varchar(255) NOT NULL,
        description_vector VECTOR(DOUBLE, 384) NOT NULL,
        PRIMARY KEY (question_id, id))
    """)

    cursor.execute("""
        CREATE TABLE session (
        name varchar(255) PRIMARY KEY)
    """)

    cursor.execute("""
        CREATE TABLE session_history (
        session_name varchar(255) references session (name),
        record_time TIMESTAMP,
        user_role varchar(255) NOT NULL,
        system BIT NOT NULL,
        record varchar(2047) NOT NULL,
        PRIMARY KEY (session_name, record_time))
    """)

    cursor.execute("""
        CREATE TABLE session_qn_ans (
        session_name varchar(255) references session (name),
        question_id INT references question (id),
        option_id INT NOT NULL,
        summary varchar(2047) NOT NULL,
        PRIMARY KEY (session_name, question_id),
        FOREIGN KEY (question_id, option_id) references question_option (question_id, id))
    """)

    print("Table creation complete.")


# Populate database with data from dataframe as a batch using SQL
    sql_add_data = f"""
        INSERT INTO question
        (id, name)
        VALUES (?, ?)
    """
    data = [(qn_num, qn_group['Question'].iloc[0])
            for qn_num, qn_group in df.groupby('Question_number')]

    cursor.executemany(sql_add_data, data)

# Populate database with data from dataframe as a batch using SQL
    sql_add_data = f"""
        INSERT INTO question_option
        (question_id, id, description, description_vector)
        VALUES (?, ?, ?, TO_VECTOR(?))
    """

# Prepare list of tuples (parameter for each row)
    data = []
    for qn_num, qn_group in df.groupby('Question_number'):
        # Add options with enumeration
        for i, row in enumerate(qn_group.itertuples()):
            data.append((
                qn_num,
                i,
                row.Options,
                str(row.Options_vector)
            ))

    cursor.executemany(sql_add_data, data)

    print("Data insertion complete.")
