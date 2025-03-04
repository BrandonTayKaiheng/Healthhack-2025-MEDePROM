# This file contains the algorithm to retrieve questions in order from the database
# The questions and options retrieved are stored into a struct to be passed to LLM

import iris
import os

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

# Question retieval algorithm
# Initialize the question number tracker
qn_num = 0

# Define table name
table_name = "ePROM_DB"

# Define sql query
qn_retrieve_query = f""" 

    SELECT DISTINCT Question
    FROM {table_name}
    WHERE Question_number = ?
    LIMIT 1;
    """

# Loop through the total number of questions 
# Modify loop based on LLM API integration 
while (qn_num < 5):
    cursor.execute(qn_retrieve_query, (qn_num,))
    results = cursor.fetchall()

    if not results:
        print("All questions asked")

    # Extract the question and options
    question = results[0][0]  # Question is the same for all rows
    options = [row[1] for row in results]  # Collect all options

    # Create a struct to be passed to LLM 
    question_object = {
        "question_number": qn_num,
        "question": question,
        "options": options
    }

    ## INSERT LLM LOGIC HERE ##
