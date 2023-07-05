import ast
import subprocess
import sys

#Basic import scanning. Determines if the import is a default python module, a pip package, or not found.

# TODO: 
# - support for local imports (e.g. from . import file)
# - Test aliased imports (e.g. import numpy as np)
# - Support for import * (e.g. from numpy import *)
# - Recursive import scanning from local imports (e.g. import <local_module> also should scan <local_module> for imports and list them)
# - (Later) Import cleanup. E.g. if a package is imported but not used, it should be removed from the import list.
# Additionally, if a package is imported but only a subset of its functions are used, it should be changed to only import those functions. 
# (e.g. from numpy import array, zeros, ones)
# - (Later) Auto requirements.txt + dockerfile generation. If a package is imported, it should be added to the dockerfile.



def get_imports(file_path):
    imports = []

    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append(f'{name.name}')
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                for name in node.names:
                    imports.append(f'{node.module}.{name.name}')

    return imports

def get_package_info(import_list):
    package_info = {}

    for package_name in import_list:
        if package_name in sys.modules or package_name.split(".")[0] in sys.modules:
            package_info[package_name] = f'Default Python module: {package_name}'
        else:
            result = subprocess.run(['pip3', 'show', package_name.split(".")[0]], capture_output=True, text=True)
            output = result.stdout.strip()

            if result.returncode == 0:
                package_info[package_name] = output
            else:
                package_info[package_name] = f'Package "{package_name}" not found.'

    return package_info


import_list = get_imports("file.py")
package_info = get_package_info(import_list)

for package_name, info in package_info.items():
    print(f'Package: {package_name}')
    print(info)
    print('------------------------')