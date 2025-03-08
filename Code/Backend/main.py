import os
import json
from DBhelpers import connect_to_IRIS, retrieve_data, similarity_search
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Connect to IRIS Database 
## Go to Docker and start IRIS instance before running this code section 

# Credentials 
username = 'demo'
password = 'demo'
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
port = '1972' 
namespace = 'USER'

cursor = connect_to_IRIS(username, password, hostname, port, namespace)
exit()

# Load Database
with open("PROM Corpus/EQ-5D-5L_corpus.json") as file:
    data = json.load(file)

# Connect to Gemini
load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

# Initialize Chat
chat = client.chats.create(
    model="gemini-2.0-flash",
    # stop sequences signal to genai the end of the conversation. they will wrap up and return 1 final response
    config=types.GenerateContentConfig(stop_sequences=["exit", "bye", "goodbye", "stop"])
    )


def retrieve_question_object(qn_num):
    return data[qn_num]

def give_instruction():
    chat.send_message(
        """You are clinical doctor collecting electronic Patient Reported Outcomes (ePROs) 
            to improve healthcare quality and enhance patients' quality of life post-procedure. 
            Interview question style must be conversational, empathetic, and encourage higher levels of self disclosure.
            Ask follow up questions until you are able to get a satisfactory answer from the patient. 
            """
        )
                      
def generate_prompt(qn_num):
    question_object = retrieve_question_object(qn_num)
    return f"""Please ask the patient about {question_object['question']}.
            You can refer to these possible answers {question_object['options']}. 
            Now, start this conversation with the patient"""


# parameters: msg: string
# return: response: string
def send_msg_to_genai(msg):
    response = chat.send_message(msg)
    return response.text
# parameters: msg: string
# return: response: None
def display_msg_to_user(msg):
    print(msg)

# parameters: None
# return: response: string
def get_response_from_user():
    response = input("User: ")

    # implement save_response_to_database(response)

    return response
    
# Start Chat
def start_chat(chat):
    give_instruction()
    for qns in range(0, 5):
        response = chat.send_message(generate_prompt(qns))
        display_msg_to_user(response.text)
        for rounds in range(0, 3):
            user_response = get_response_from_user()
            # "exit" is a hard stop to terminate the program immediately
            if user_response == "exit":
                return
            response = send_msg_to_genai(user_response)
            display_msg_to_user(response)


start_chat(chat)

