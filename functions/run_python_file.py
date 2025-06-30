import os
import subprocess


def run_python_file(working_directory, file_path):
    path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(path):
        return f'Error: File "{file_path}" not found.'
    if not os.path.abspath(path).endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(
            ["python3", os.path.abspath(path)],
            cwd=os.path.abspath(working_directory),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        if not result.stdout and not result.stderr:
            return f'No output produced.'

        output = f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}\n'
        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}\n'
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"