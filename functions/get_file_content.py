import os
from config import READ_LIMIT

def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)

    # Join might now be necessary here since technically we are just
    # adding a file onto the end of the abs path
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Read the file 
    # If file length > 10000 truncate to 10000 and append
    # [...File "{file_path}" truncated at 10000 characters] to the end
    # READ_LIMIT is set by config.py 

    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(READ_LIMIT)
            
            if len(file_content_string) == READ_LIMIT:
                truncation_str = f'[...File "{file_path}" truncated at {READ_LIMIT} characters]'
                file_content_string += truncation_str

            return file_content_string

    except Exception as e:
        return f'Error: {e}'
