import subprocess
import sys


required_modules = [
    "pathlib",
    "time","tkinter","random",
    "datetime",
    "pymysql",
    "paho.mqtt",
    "tkcalendar",
    "reportlab",
    "datetime",
    "pyserial",
    "db-sqlite3"
]
#"time","tkinter","random","NIGGER","NIGGERlittle",
sucful=[]
unsucful=[]
def install_modules(modules):

    for module in modules:
        try:
            print(f"Installing {module}...")
            subprocess.check_call(["pip", "install", module])
            print(f"Successfully installed {module}.")
            sucful.append(module)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {module}: {e}")
            unsucful.append(module)
    print("\n")

    if len(sucful) == len(required_modules):
        print("-------------------------\nInstallation Report :\n")
        print('''SuccessfulL installed all the modules : DONE\n-------------------------''')
    else:
        print("-------------------------\nInstallation Report :\n")
        print("UnSuccessfully!!!  = ", unsucful)
        print("Successfull  = ", sucful)
        print("-------------------------\n")

def check_imports(required_modules):
    missing_modules=[]

    print("Importing Report :\n")
    for module_name in required_modules:
        try:
            __import__(module_name)
            print(f" Module '{module_name}' installed and importable : DONE")
        except ImportError:
            missing_modules.append(module_name)
            print(f" ---> Import error for '{module_name}' : ERROR")
    print("-------------------------")



install_modules(required_modules)
#print("checking for Imports\n")
check_imports(required_modules)



