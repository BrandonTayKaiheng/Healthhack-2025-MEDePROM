from google import genai
from google.genai import types
from model.tools import control_flow_tools


class Chatbot:
    client = None
    dbcontext = None
    model = "gemini-2.0-flash-001"
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        # top_p=0.5,
        # max_output_tokens=8192,
        # safety_settings=[types.SafetySetting(
        #     category="HARM_CATEGORY_HATE_SPEECH",
        #     threshold="OFF"
        # ), types.SafetySetting(
        #     category="HARM_CATEGORY_DANGEROUS_CONTENT",
        #     threshold="OFF"
        # ), types.SafetySetting(
        #     category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
        #     threshold="OFF"
        # ), types.SafetySetting(
        #     category="HARM_CATEGORY_HARASSMENT",
        #     threshold="OFF"
        # )],
        # Function signatures for tool calling.
        # Comment out the tools config below to disable function calling.
        # tools=[
        #     control_flow_tools
        # ]
    )

    def __init__(self, dbcontext):
        if Chatbot.client is None:
            Chatbot.client = genai.Client(
                vertexai=True,
                project="health-hack-2025",
                location="us-west1",

                # API key authentication is not supported by vertex ai.
                # Instead, authenticate using Google ADC.
                # api_key=gemini_apik_key
            )
            Chatbot.dbcontext = dbcontext

    def create_session(self):
        pass

    def test(self):
        response = Chatbot.client.models.generate_content(
            model=Chatbot.model,
            contents="""You are clinical doctor collecting electronic Patient Reported Outcomes (ePROs) 
                to improve healthcare quality and enhance patients' quality of life post-procedure. 
                Interview question style must be conversational, empathetic, and encourage higher levels of self disclosure.
                Ask follow up questions until you are able to get a satisfactory answer from the patient. 
                """
            +
            """Please ask the patient about his mobility.
                Now, start this conversation with the patient""",
            config=Chatbot.generate_content_config
        )
        return response.text
#
#     def give_instruction():
#         chat.send_message(
#             """You are clinical doctor collecting electronic Patient Reported Outcomes (ePROs)
#                 to improve healthcare quality and enhance patients' quality of life post-procedure.
#                 Interview question style must be conversational, empathetic, and encourage higher levels of self disclosure.
#                 Ask follow up questions until you are able to get a satisfactory answer from the patient.
#                 """
#         )
#
#     def generate_prompt(qn_num):
#         question_object = Chatbot.dbcontext.get_question_options(qn_num)
#         return f"""Please ask the patient about {question_object['question']}.
#                 You can refer to these possible answers {question_object['options']}.
#                 Now, start this conversation with the patient"""
#
#
# # parameters: msg: string
# # return: response: string
# def send_msg_to_genai(msg):
#     response = chat.send_message(msg)
#     return response.text
# # parameters: msg: string
# # return: response: None
#
#
# def display_msg_to_user(msg):
#     print(msg)
#
# # parameters: None
# # return: response: string
#
#
# def get_response_from_user():
#     response = input("User: ")
#
#     # implement save_response_to_database(response)
#
#     return response
#
# # Start Chat
#
#
# def start_chat(chat):
#     give_instruction()
#     for qns in range(0, 5):
#         response = chat.send_message(generate_prompt(qns))
#         display_msg_to_user(response.text)
#         for rounds in range(0, 3):
#             user_response = get_response_from_user()
#             # "exit" is a hard stop to terminate the program immediately
#             if user_response == "exit":
#                 return
#             response = send_msg_to_genai(user_response)
#             display_msg_to_user(response)
#
#
# start_chat(chat)
