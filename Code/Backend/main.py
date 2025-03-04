import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

chat = client.chats.create(model="gemini-2.0-flash")
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents="Explain how AI works",
# )

# print(response.text)
while True:
    prompt = input("You: ")
    if (prompt == "exit"):
        break
    # print(f"Hello, {prompt}")
    response = chat.send_message(prompt)

    print(response.text)
    # for message in chat._curated_history:
    #     print(f"role - {message.role}", end=": ")
    #     print(message.parts[0].text)