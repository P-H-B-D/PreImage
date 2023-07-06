import ast
import subprocess
import sys
import os
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


#Hierarchy of checking imports (TODO: add support for submodules in recursive import scanning case):
# 1. Check if the import is a default python module
# 2. Check if the import is a pip package
# 3. Check if the import is a local import
# Fallthrough: If none of the above, the import is not found.


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
            package_info[package_name] = f'D: {package_name}'
        else:
            result = subprocess.run(['pip3', 'show', package_name.split(".")[0]], capture_output=True, text=True)
            output = result.stdout.strip()

            if result.returncode == 0:
                package_info[package_name] = f'P: {output}' #Pip package
            else:
                if os.path.exists(package_name.split(".")[0]+".py"):
                    package_info[package_name] = f'L: {package_name}' #Local import 
                else:
                    package_info[package_name] = f'N: "{package_name}" not found.' #Package not found

    return package_info


# def imports_from_path(target,numindent=0):

#     import_list = get_imports(target)
#     print(numindent*"\t"+target+" imports:")
#     print(numindent*"\t"+'------------------------')
#     package_info = get_package_info(import_list)

#     for package_name, info in package_info.items():
#         prefix=info[0:1]
#         # print(f'{info}')
#         print(numindent*"\t"+prefix)
#         if(prefix=="D"): #Default python module
#             print(numindent*"\t"+'default python module')
#             print(numindent*"\t"+info[3:])
            
#         elif(prefix=="P"): #Pip package
#             print(numindent*"\t"+'pip package')
#             print(numindent*"\t"+info.split("Location: ")[1].split("\n")[0].strip()+"/"+package_name)
#         elif(prefix=="L"): #Local import
#             print(numindent*"\t"+'local import')
#             print(numindent*"\t"+info[3:])
#             if("." in package_name):
#                 print(numindent*"\t"+os.path.abspath(package_name.split(".")[0]+".py"))
#                 #should add recursion here
#                 imports_from_path(os.path.abspath(package_name.split(".")[0]+".py"),numindent+1)


#             else:
#                 print(numindent*"\t"+os.path.abspath(package_name))
#         elif(prefix=="N"): #Package not found
#             print(numindent*"\t"+'package not found')
#         else:
#             raise Exception("Invalid prefix")
#         print(numindent*"\t"+'------------------------')

def imports_from_path(target, numindent=0, prefix=''):
    import_list = get_imports(target)
    print(numindent * "\t" + prefix + target)
    for package_name in import_list:
        info = get_package_info([package_name])[package_name]
        subprefix = "├─ " if package_name != import_list[-1] else "└─ "
        subprefix += "D: " if info.startswith("D") else ""
        subprefix += "P: " if info.startswith("P") else ""
        subprefix += "L: " if info.startswith("L") else ""
        subprefix += "N: " if info.startswith("N") else ""
        print((numindent + 1) * "\t" + subprefix + package_name)
        if info.startswith("L"):
            if "." in package_name:
                path = os.path.abspath(package_name.split(".")[0] + ".py")
                imports_from_path(path, numindent + 2, "│  ")
            else:
                path = os.path.abspath(package_name)
                imports_from_path(path, numindent + 2, "│  ")

    print()

target="file.py"
imports_from_path(target)