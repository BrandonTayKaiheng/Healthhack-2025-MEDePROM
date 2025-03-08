import inspect
import docstring_parser

from vertexai.generative_models import (
    FunctionDeclaration,
    Tool,
)


def generate_tool(func):
    """
    Generate an OpenAI-compatible function schema from a Python function.
    """
    # Get function name
    name = func.__name__

    # Get function docstring and parse it
    docstring = inspect.getdoc(func) or ""
    parsed_docstring = docstring_parser.parse(docstring)

    # Extract description from docstring
    description = parsed_docstring.short_description or "No description available"

    # Get function signature
    signature = inspect.signature(func)

    # Create parameters schema
    properties = {}
    required = []

    for param_name, param in signature.parameters.items():
        # Skip self for class methods
        if param_name == "self":
            continue

        param_info = {"type": "string"}  # Default type

        # Try to determine parameter type from type annotations
        if param.annotation != inspect.Parameter.empty:
            param_type = param.annotation
            if param_type == str:
                param_info["type"] = "string"
            elif param_type == int:
                param_info["type"] = "integer"
            elif param_type == float:
                param_info["type"] = "number"
            elif param_type == bool:
                param_info["type"] = "boolean"
            elif param_type == list or (hasattr(param_type, "__origin__") and param_type.__origin__ == list):
                param_info["type"] = "array"
            elif param_type == dict or (hasattr(param_type, "__origin__") and param_type.__origin__ == dict):
                param_info["type"] = "object"

        # Look for parameter description in docstring
        param_description = None
        for param_doc in parsed_docstring.params:
            if param_doc.arg_name == param_name:
                param_description = param_doc.description
                break

        if param_description:
            param_info["description"] = param_description

        # Add parameter to properties
        properties[param_name] = param_info

        # Check if parameter is required (no default value)
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    # Build the complete schema
    tool = FunctionDeclaration(
        name=name,
        descriptio=description,
        parameters={
            "type": "object",
            "properties": properties
        }
    )

    print(name, description, properties)

    return tool


def generate_tools_for_module():
    """Generate tools based on all functions in a module."""
    tools = []

    for name, obj in inspect.getmembers("./tools.py"):
        print(name, obj)
        # Only process functions (not built-ins, classes, etc.)
        if inspect.isfunction(obj) and not name.startswith("_"):
            tools.append(generate_tool(obj))

    return Tool(function_declarations=tools)


print(generate_tools_for_module())
