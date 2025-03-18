from datetime import datetime
from dataclasses import dataclass, field
from typing import List
from google import genai
from google.genai import types
from google.genai.types import FunctionCallingConfig
from models.questions import Question, QuestionOption
from chatbot.tools import control_flow_tools


class Chatbot:
    client = None
    dbcontext = None
    sessions = {}

    model = "gemini-2.0-flash-001"
    sys_instruct = """You are a bot, tasked with helping clinical doctors with collecting electronic
                Patient Reported Outcomes (ePROs) to improve healthcare quality and enhance patients'
                quality of life post-procedure.
                Ask the user questions based on the ePRO survey questions provided by the system.
                Interview question style must be conversational, empathetic, and encourage higher levels of self disclosure.
                Be inquisitive and always ask follow up questions about any concerns the patient raise.
                Do not move onto the next question in the survey until instruction has been given."""
    generate_content_config = types.GenerateContentConfig(
        temperature=0.95,
        top_p=0.95,
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
        system_instruction=sys_instruct,
        tools=[
            control_flow_tools
        ],
    )
    function_calling_config = types.GenerateContentConfig(
        temperature=0,
        tools=[
            control_flow_tools
        ],
        # tool_config=types.ToolConfig(
        #     function_calling_config=types.FunctionCallingConfig(
        # ANY mode forces the model to predict only function calls
        # mode=FunctionCallingConfig.  # ask)
        # )
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
            questions = Chatbot.dbcontext.get_all_questions()
            s = Session(name=name, questions=questions)
            Chatbot.sessions[name] = s
            Chatbot.dbcontext.create_session(name)
        return s

    def get_session(self, name):
        return Chatbot.sessions.get(name)

    def create_chat(self):
        return Chatbot.client.chats.create(
            model="gemini-2.0-flash",
            # stop sequences signal to genai the end of the conversation. they will wrap up and return 1 final response
            config=Chatbot.generate_content_config
        )


@dataclass
class Session:
    name: str
    questions: List[Question]
    answers: List[QuestionOption] = field(default_factory=list)
    all_history: List[types.Content] = field(default_factory=list)
    curr_qn_history: List[types.Content] = field(default_factory=list)
    current_question_index: int = field(default=0)

    def start(self):
        if not self.all_history:
            current_question = self.get_current_question()
            if not current_question:
                return "You have reached the end of the survey! Thank you so much for your feedback."

            # start_prompt="You will be asking the patient these questions for this ePRO survey:\n"
            # for qn in self.questions:
            #     start_prompt += qn.name
            #     if qn.description:
            #         start_prompt += "Description: " + qn.description
            #     start_prompt += "\n"

            question_options = Chatbot.dbcontext.get_question_options(
                current_question.id)

            start_prompt = f"""Firstly, introduce yourself, then start by asking the patient about:
            {current_question.name}{"Description: " + current_question.description if current_question.description else ""}.
            You can refer to these possible answers: {[q.description for q in question_options]}.
            Do not quote the options directly.
            Now, start this conversation with the patient."""

            self.record_history("user", True, start_prompt)

            response = Chatbot.client.models.generate_content(
                model=Chatbot.model,
                contents=self.all_history,
                config=Chatbot.generate_content_config
            )

            self.record_history("model", False, response.text)
            return response.text

    def send_message(self, user_input):
        self.record_history("user", False, user_input)

        # function = Chatbot.client.models.generate_content(
        #     model=Chatbot.model,
        #     contents=self.curr_qn_history,
        #     config=Chatbot.function_calling_config
        # )
        #
        # print(function.candidates[0].content.parts)
        #
        # if function.function_calls and function.function_calls[0].name == "valuate_quantitative_response":
        #     args = function.function_calls[0].args
        #
        #     if args.get("response"):
        #         response = args.get("response")
        #     else:
        #         response = "\n".join([r.text for r in filter(
        #             lambda h: h.role == "user", self.curr_qn_history)])
        #
        #     if args.get("summary"):
        #         summary = args.get("summary")
        #     else:
        #         summary = ""
        #
        #     Chatbot.dbcontext.save_session_ans(
        #         self.name, self.current_question_index, response, summary)
        #
        #     self.curr_qn_history = []
        #
        #     have_next = self.move_to_next_question()
        #
        #     if have_next:
        #         current_question = self.get_current_question()
        #         question_options = Chatbot.dbcontext.get_question_options(
        #             current_question.id)
        #
        #         prompt = f"""Next, ask the patient about:
        #         {current_question.name}{"Description: " + current_question.description if current_question.description else ""}.
        #         You can refer to these possible answers: {[q.description for q in question_options]}"""
        #
        #         self.record_history("user", True, prompt)

        response = Chatbot.client.models.generate_content(
            model=Chatbot.model,
            contents=self.all_history,
            config=Chatbot.generate_content_config
        )

        print(response.candidates[0].content.parts)

        if response.function_calls and response.function_calls[0].name == "valuate_quantitative_response":
            args = response.function_calls[0].args

            if args.get("response"):
                response = args.get("response")
            else:
                response = "\n".join([r.text for r in filter(
                    lambda h: h.role == "user", self.curr_qn_history)])

            if args.get("summary"):
                summary = args.get("summary")
            else:
                summary = ""

            Chatbot.dbcontext.save_session_ans(
                self.name, self.current_question_index, response, summary)

            have_next = self.move_to_next_question()

            if have_next:
                current_question = self.get_current_question()
                question_options = Chatbot.dbcontext.get_question_options(
                    current_question.id)

                prompt = f"""Next, ask the patient about:
                {current_question.name}{"Description: " + current_question.description if current_question.description else ""}.
                You can refer to these possible answers: {[q.description for q in question_options]}
                Do not quote the options directly."""

                self.record_history("user", True, prompt)

                response = Chatbot.client.models.generate_content(
                    model=Chatbot.model,
                    contents=self.all_history,
                    config=Chatbot.generate_content_config
                )

        text = response.text

        self.record_history("model", False, text)

        return text

    def get_current_question(self):
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None

    def move_to_next_question(self):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            return True
        return False

    def record_history(self, role, system, content):

        Chatbot.dbcontext.save_session_history(
            self.name, datetime.now(), role, system, content)

        formatted_history = self._format_history(role, content)
        self.all_history.append(formatted_history)

        self.curr_qn_history.append(formatted_history)

    def _format_history(self, role, content):
        # Role must either be user or model
        return types.Content(parts=[types.Part(text=content)], role=role)
