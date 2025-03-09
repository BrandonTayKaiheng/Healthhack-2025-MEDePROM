from dataclasses import dataclass, field
from typing import List
from google import genai
from google.genai import types
from models.questions import Question, QuestionOption
from chatbot.tools import control_flow_tools


class Chatbot:
    client = None
    dbcontext = None
    sessions = {}

    model = "gemini-2.0-flash-001"
    sys_instruct = """You are clinical doctor collecting electronic Patient Reported Outcomes (ePROs) 
                to improve healthcare quality and enhance patients' quality of life post-procedure. 
                Interview question style must be conversational, empathetic, and encourage higher levels of self disclosure.
                Ask follow up questions until you are able to get a satisfactory answer from the patient."""
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.5,
        max_output_tokens=8192,
        safety_settings=[types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="OFF"
        ), types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="OFF"
        )],
    )
    function_calling_config = types.GenerateContentConfig(
        temperature=0,
        tools=[
            control_flow_tools
        ]
    )

    def __init__(self, gemini_api_key, dbcontext):
        # if the Chatbot singleton is not instantiated,
        # instatiate it once and once only
        if Chatbot.client is None:
            Chatbot.client = genai.Client(
                # vertexai=True,
                # project="health-hack-2025",
                # location="us-west1",

                # API key authentication is not supported by vertex ai.
                # Instead, authenticate using Google ADC.
                api_key=gemini_api_key
            )
            Chatbot.dbcontext = dbcontext

    def create_session(self, name):
        s = Chatbot.sessions.get(name)
        if not s:
            s = Session(name, Chatbot.dbcontext.get_all_questions())
            Chatbot.sessions[name] = s
        return s

    def get_session(self, name):
        return Chatbot.sessions.get(name)

    # def test(self):
    #     response = Chatbot.client.models.generate_content(
    #         model=Chatbot.model,
    #         contents="I am going through severe pain.",
    #         config=Chatbot.function_calling_config,
    #     )
    #     return response


@dataclass
class Session:
    name: str
    questions: List[Question]
    answers: List[QuestionOption] = field(default_factory=list)
    history: List[str] = field(default_factory=list)

    def chat(self, user_input):
        Chatbot.client.models.generate_content(

        )
