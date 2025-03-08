import vertexai
from tools import control_flow_tools

from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

# TODO(developer): Update & uncomment below line
PROJECT_ID = "health-hack-2025"
LOCATION = "us-west1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Initialize Gemini model
model = GenerativeModel("gemini-2.0-flash-001")

# Define the user's prompt in a Content object that we can reuse in model calls
user_prompt_content = Content(
    role="user",
    parts=[
        Part.from_text("I find it hard to move around."),
    ],
)


# Send the prompt and instruct the model to generate content using the Tool that you just created
response = model.generate_content(
    user_prompt_content,
    generation_config=GenerationConfig(temperature=0),
    tools=[control_flow_tools],
)
function_call = response.candidates[0].function_calls[0]
# print(function_call)
# print(response.text)
print(response.candidates)


# # Return the API response to Gemini so it can generate a model response or request another function call
# response = model.generate_content(
#     [
#         user_prompt_content,  # User prompt
#         response.candidates[0].content,  # Function call response
#         Content(
#             parts=[
#                 Part.from_function_response(
#                     name=function_name,
#                     response={
#                         "content": api_response,  # Return the API response to Gemini
#                     },
#                 ),
#             ],
#         ),
#     ],
#     tools=[weather_tool],
# )

if __name__ == "__main__":
    conversation_ongoing = True

    while conversation_ongoing
