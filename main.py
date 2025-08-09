import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("Error: No args provided\n")
        print('Usages: python main.py "your prompt here" [--verbose]')

    prompt = "".join(args)
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    if verbose:
        print((f"User prompt: {prompt}\n"))
    
    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    count = 0
    while count < 20: 
        try: 
            resp = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )

            if resp.candidates:
                for resp_candidate in resp.candidates:
                    messages.append(resp_candidate.content)


            if verbose:
                print(f"Prompt tokens: {resp.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {resp.usage_metadata.candidates_token_count}")

            if not resp.function_calls:
                print("Response:")
                print(resp.text)
                break
            else:
                for function_call_part in resp.function_calls:
                    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                    res: types.Content | None = call_function(function_call_part, verbose)
                    if res and res.parts[0].function_response.response:
                        if verbose:
                            print(f"-> {resp.parts[0].function_response.response}")
                    else:
                        sys.exit(1)

                    res.role = "tool"
                    messages.append(res)
        except Exception as e:
            print(f'Error: {e}')
        count += 1

def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.args != None:
        function_call_part.args["working_directory"] = "./calculator"
        functions = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "run_python_file": run_python_file,
            "write_file": write_file
        }

        if function_call_part.name != None:
            if function_call_part.name in functions:
                result = functions[function_call_part.name](**function_call_part.args)        
                return types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=function_call_part.name,
                                response={"result": result}
                        )
                    ],
                ) 

            else:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"error": f"Unknown function: {function_call_part.name}"},
                        )
                    ],
                )

if __name__ == "__main__":
    main()
