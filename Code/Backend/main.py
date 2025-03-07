import os
import json
from DBhelpers.py import *
from google import genai
from dotenv import load_dotenv

## Connecting to IRIS Database 
# Go to Docker and start IRIS instance before running this code section 

# Credentials 
username = 'demo'
password = 'demo'
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
port = '1972' 
namespace = 'USER'


# with open("PROM Corpus/EQ-5D-5L_corpus.json") as file:
#     data = json.load(file)

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

chat = client.chats.create(model="gemini-2.0-flash")
connect_to_IRIS(username, password, hostname, port, namespace)

# initial_prompt = f"You are a chatbot collecting Patient Reported Outcomes (PROs) EQ-5D-5L_corpus. Please ask the patient the following questions: {data[0]["question"]}"

# response = chat.send_message(initial_prompt)
# print(response.text)
# while True:
#     new_prompt = input("You: ")
#     if new_prompt == "exit":
#         break
#     response = chat.send_message(new_prompt)
#     print(response.text)
