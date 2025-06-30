import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.call_function import call_function

if len(sys.argv) >= 2:
    user_prompt = sys.argv[1]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


    schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="""Reads the contents of a specified file (relative to the working directory), up to 10,000 characters. Returns an error if the file does not exist, 
        is not a regular file, or is outside the permitted working directory. If the file is longer than 10,000 characters, the output is truncated and a notice is appended.""",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to read from, should be in the working directory. If not provided, Read returns a not found message."
                ),
            },
            required=["file_path"],
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file (relative to the working directory) and returns its stdout and stderr output. Only .py files inside the working directory are allowed.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The Python file to run, relative to the working directory.",
                ),
            },
            required=["file_path"],
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description=(
            "Writes content to a specified file (relative to the working directory). "
            "If the file does not exist, it is created. If the file exists, it is overwritten. "
            "Returns an error if the file is outside the permitted working directory."
        ),
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write to, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
            required=["file_path", "content"],
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    verbose = (len(sys.argv) == 3 and sys.argv[2] == "--verbose")

    for i in range(20):
        response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        for elem in response.candidates:
            messages.append(elem.content)
        
        if not response.function_calls:
            print(response.text)
            break
        else:
            call_func = call_function(response.function_calls[0], verbose=verbose)

            if not call_func.parts[0].function_response.response:
                raise Exception("ERROR")
            else:
                if verbose:
                    print(f"-> {call_func.parts[0].function_response.response}")
                    print(f"User prompt: {user_prompt}")
                    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
                messages.append(call_func)


else:
    print("You should execute the script like this: <<python3 file.py `What You want to ask about.`>>")
    sys.exit(1)
