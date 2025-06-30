# from functions.get_file_content import get_file_content
# from functions.write_file import write_file
from functions.run_python_file import run_python_file


# print('Testing get_file_content("calculator", "lorem.txt")')
# content1 = get_file_content("calculator", "lorem.txt")
# print(content1)

# print('Testing get_file_content("calculator", "main.py")')
# content2 = get_file_content("calculator", "main.py")
# print(content2)

# print('Testing get_file_content("calculator", "pkg/calculator.py")')
# content3 = get_file_content("calculator", "pkg/calculator.py")
# print(content3)

# print('Testing get_file_content("calculator", "/bin/cat")')
# content4 = get_file_content("calculator", "/bin/cat")
# print(content4)

# print('Testing write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum")')
# result1 =write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
# print(result1)

# print('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")')
# result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
# print(result2)

# print('write_file("calculator", "/tmp/temp.txt", "this should not be allowed")')
# result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
# print(result3)

print('run_python_file("calculator", "main.py")')
run1 = run_python_file("calculator", "main.py")
print(run1)

print('run_python_file("calculator", "tests.py")')
run2 = run_python_file("calculator", "tests.py")
print(run2)

print('run_python_file("calculator", "../main.py")')
run3 = run_python_file("calculator", "../main.py")
print(run3)

print('run_python_file("calculator", "nonexistent.py")')
run4 = run_python_file("calculator", "nonexistent.py")
print(run4)
