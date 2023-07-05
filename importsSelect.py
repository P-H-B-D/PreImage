import ast

def get_imports(file_content):
    """
    Recursively finds all imports in a Python file.
    Returns a list of imported module names.
    """
    imports = []

    def visit_Import(node):
        for alias in node.names:
            imports.append(alias.name)

    def visit_ImportFrom(node):
        for alias in node.names:
            if node.module:
                imports.append(f"{node.module}.{alias.name}")
            else:
                imports.append(alias.name)

    tree = ast.parse(file_content)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            visit_Import(node)
        elif isinstance(node, ast.ImportFrom):
            visit_ImportFrom(node)

    return imports
