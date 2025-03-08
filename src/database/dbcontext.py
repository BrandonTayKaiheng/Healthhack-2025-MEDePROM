import iris
import os
from utils.vectorisor import vectorise

# Connect to database
# Go to Docker and start IRIS instance before running this code section

# Credentials
# username = 'demo'
# password = 'demo'
# hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
# port = '1972'
# namespace = 'USER'

# qn_num = 0
# table_name = "ePROM_DB"

# Connect to IRIS
# Go to Docker and start IRIS instance before running this code section


class DbContext:
    cursor = None

    def __init__(self, username, password, hostname, port, namespace):
        if DbContext.cursor is None:
            print("No existing IRIS connection. Instantiating new connection.")
            # Concat connection string
            CONNECTION_STRING = f"{hostname}:{port}/{namespace}"

            # Connect to IRIS
            connect = iris.connect(CONNECTION_STRING, username, password)
            try:
                DbContext.cursor = connect.cursor()
                print("Successfully connected to IRIS")
            except Exception:
                print("""
                    Connection to IRIS failed.
                    Is your IRIS instance is running on Docker?
                    """)

    def retrieve_data(self, qn_num, table_name):
        # Define sql query
        qn_retrieve_query = f"""
            SELECT DISTINCT Question
            FROM {table_name}
            WHERE Question_number = ?;
            """

        # Loop through the total number of questions
        # The questions and options retrieved are stored into a dictionary to be passed to LLM
        DbContext.cursor.execute(qn_retrieve_query, (qn_num,))
        results = DbContext.cursor.fetchall()

        print(results)

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
        return question_object

# Vectorize the patient's response for the question using Transformer model
# Execute vector dot product similarity search

    def similarity_search(self, query_phrase, table_name, number_of_results, cursor):

        # Load pretrained Transformer model (we use 'all-MiniLM-L6-v2' lightweight multipurpose, can change later)

        # Define SQL query
        sql = f"""
            SELECT TOP ? Question_number, Question, Option,
            FROM {table_name}
            ORDER BY VECTOR_DOT_PRODUCT(Option_vector, TO_VECTOR(?)) DESC
        """
        # Embed query phrase into
        # Vectorize search phrase
        query_vector = vectorise(query_phrase)

        # Execute SQL query
        cursor.execute(sql, [number_of_results, str(query_vector)])

        # Fetch results
        results = cursor.fetchall()
        for i in results:
            print(i)

        return results
