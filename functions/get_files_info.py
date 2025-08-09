import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory) 
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        dir_content = os.listdir(target_dir)
        content = [] 
        for item in dir_content:
            join_item_path = os.path.join(target_dir, item)
            size = os.path.getsize(join_item_path)
            is_dir = os.path.isdir(join_item_path)
            content.append(f"- {item}: file_size={size}, is_dir={is_dir}") 
    except Exception as e:
        return f'Error: {e}'

    return "\n".join(content)


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

