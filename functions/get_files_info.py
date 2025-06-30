import os


def get_files_info(working_directory, directory=None):
    if directory is None:
        path = working_directory
    else:
        path = os.path.join(working_directory, directory)
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(os.path.abspath(path)):
        return f'Error: "{directory}" is not a directory'
    try:
        string = ""
        dir_content = os.listdir(path)
        for content in dir_content:
            string += f"- {content}: file_size={os.path.getsize(os.path.abspath((os.path.join(path, content))))} bytes, is_dir={os.path.isdir(os.path.abspath((os.path.join(path, content))))}\n"
        return string
    except Exception as e:
        return f"Error: {e}"
