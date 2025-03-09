# Specify a function declaration and parameters for an API request
from google.genai.types import FunctionDeclaration, Tool


# Specify a function declaration and parameters for an API request

valuate_quantitative_response_func = FunctionDeclaration(
    name="valuate_quantitative_response",
    description="""Matches the patients reponse to a quantitative level.
    This should be called when the patient's response to
    the PROM question is somewhat quantifiable.""",
    # Function parameters are specified in JSON schema format
    parameters={
        "type": "object",
        "properties": {"response": {"type": "string",
                                    "description": "Patient's response to the question."}},
    },
)

# Specify a function declaration and parameters for an API request
further_probe_patient_func = FunctionDeclaration(
    name="further_probe_patient",
    description="Probe the patient further on concerns that they have raised.",
    # Function parameters are specified in JSON schema format
    parameters={
        "type": "object",
        "properties": {"concerns": {"type": "string",
                                    "description": "Concerns that the patient has raised."}}
    },
)

# Define a tool that includes the above get_current_weather_func
control_flow_tools = Tool(
    function_declarations=[
        valuate_quantitative_response_func, further_probe_patient_func],
)


def valuate_quantitative_response(response: str) -> None:
    """Matches the patients reponse to a quantitative level.
    This should be called when the patient's response to
    the PROM question is somewhat quantifiable.

    :param response: Patient's response to the question.
    """
    # performs a vector search with the db and finds the most liekly qualitative response.
