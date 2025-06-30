import os


def get_file_content(working_directory, file_path):
    path = os.path.join(working_directory, file_path)
    MAX_CHARS = 10000
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(os.path.abspath(path)):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(os.path.abspath(path), "r") as f:
            file_content_string = f.read(MAX_CHARS)
            remainder = f.read(1)
            if remainder:
                file_content_string += f'\n[...File "{os.path.abspath(path)}" truncated at 10000 characters]'
            return file_content_string
    except Exception as e:
        return f"Error: {e}"
    
