import iris
import os
from utils.vectorisor import vectorise
from dataclasses import dataclass


@dataclass
class Question:
    id: int
    name: str
    description: str | None


@dataclass
class QuestionOption:
    question_id: int
    id: int
    rating: int | None
    label: str | None
    description: str


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

    def get_all_questions(self):
        get_all_qn_query = """
            SELECT id, name, description
            FROM question
            """
        DbContext.cursor.execute(get_all_qn_query)
        results = DbContext.cursor.fetchall()

        return [Question(*q) for q in results]

    def get_question_options(self, qn_num):
        # Define sql query
        get_qn_query = """
            SELECT id, rating, label, description
            FROM question_option
            WHERE question_id = ?
            """

        DbContext.cursor.execute(get_qn_query, (qn_num,))
        results = DbContext.cursor.fetchall()

        return [QuestionOption(qn_num, *q) for q in results]

    def search_question_option(self, qn_num, query_phrase, number_of_results):
        # Vectorize the patient's response for the question using Transformer model
        # Execute vector dot product similarity search

        # Define SQL query
        sql = """
            SELECT TOP ?
                id,
                VECTOR_DOT_PRODUCT(description_vector, TO_VECTOR(?))
                    AS similarity_score
            FROM question_option
            WHERE question_id = ?
            ORDER BY similarity_score DESC
        """
        # Embed query phrase into
        # Vectorize search phrase
        query_vector = vectorise(query_phrase)

        # Execute SQL query
        DbContext.cursor.execute(
            sql, [number_of_results, qn_num, str(query_vector)])
        results = DbContext.cursor.fetchall()
        for i in results:
            print(i)

        return results
