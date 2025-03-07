import os
import json
# from DBhelpers.py import *
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

# connect_to_IRIS(username, password, hostname, port, namespace)

# Load Database
with open("PROM Corpus/EQ-5D-5L_corpus.json") as file:
    data = json.load(file)

# Connect to Gemini
load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

# Initialize Chat
chat = client.chats.create(model="gemini-2.0-flash")


def retrieve_question_object(qn_num):
    return data[qn_num]

def generate_prompt(qn_num):
    question_object = retrieve_question_object(qn_num)
    return f"""You are clinical doctor collecting electronic Patient Reported Outcomes (ePROs) 
            to improve healthcare quality and enhance patients' quality of life post-procedure. 
            Interview question style must be conversational, empathetic, and encourage higher levels of self disclosure.
            Please ask the patient about {question_object['question']}.
            These are the answers you can expect: {question_object['options']}
            Ask follow up questions until you are able to get a satisfactory answer from the patient. 
            Pretend you are starting this conversation with the patient, who will be answering your questions one by one"""


# parameters: chat, msg: string
# return: response: string
def send_msg_to_genai(chat, msg):
    pass
# parameters: msg: string
# return: response: None
def display_msg_to_user(msg):
    pass
# parameters: None
# return: response: string
def get_response_from_user():
    pass
    
# Start Chat
def start_chat(chat):
    response = chat.send_message(generate_prompt(0))
    print(response.text)
    while True:
        new_prompt = input("You: ")
        if new_prompt == "exit":
            break
        response = chat.send_message(new_prompt)
        print(response.text)


start_chat(chat)
# while True:
#     new_prompt = input("You: ")
#     if new_prompt == "exit":
#         break
#     response = chat.send_message(new_prompt)
#     print(response.text)
