import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_path = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: File "{file_path}" not found.'
    
    if not target_file.endswith(".py"): 
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(["python", target_file, *args], stdin=True, stderr=True, timeout=30)
        
        output = ''
        if completed_process.stdout != '':
            output += f'STDOUT: {completed_process.stdout}\n'

        if completed_process.stderr != '':
            output += f'STDERR: {completed_process.stderr}\n'

        if completed_process.returncode != 0:
            output += f'Process exited with code {completed_process.returncode}\n'

        if output == '':
            return f'No output produced.'

        return output

    except Exception as e:
        return f'Error: executing Python file: {e}'

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run. If not provided, errors out.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING), 
                description="An array of arguments to pass in with. Example --verbose to see more messages.",),
        },
    ),
)
