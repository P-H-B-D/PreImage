from importsSelect import get_imports
with open('file.py', 'r') as file:
    file_content = file.read()

imported_modules = get_imports(file_content)
print(imported_modules)
