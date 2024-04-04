import argparse
import os
import subprocess
import sys

def create_venv(venv):
    """
    Create a virtual environment if it doesn't exist.
    """
    if not os.path.exists(venv):
        print(f"Creating virtual environment at {venv}")
        subprocess.check_call([sys.executable, "-m", "venv", venv])
    else:
        print("Virtual environment already exists.")
    return os.path.join(venv, "bin", "python") if os.name != "nt" else os.path.join(venv, "Scripts", "python.exe"), os.path.join(venv, "bin", 'playwright') 

def install_packages(venv_python, requirements_path):
    """
    Install packages from a requirements.txt file using pip in the virtual environment.
    """
    print(f"Installing packages from {requirements_path}...")
    subprocess.check_call([venv_python, "-m", "pip", "install", "-r", requirements_path])

def install_playwright(venv_playwright):
    """
    Install playwright in the virtual environment.
    """
    print(f"Installing playwright...")
    subprocess.check_call([venv_playwright, "install"])

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Create a virtual environment and install packages from requirements.txt.")
    parser.add_argument("--venv", help="The directory where the virtual environment will be created.")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    venv_python, venv_playwright = create_venv(args.venv)

    # Assuming the requirements.txt file is in the same directory as this script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    requirements_path = os.path.join(script_dir, "requirements.txt")
    
    if os.path.isfile(requirements_path):
        install_packages(venv_python, requirements_path)
    else:
        print(f"Error: requirements.txt file not found in {script_dir}")
        sys.exit(1)

    install_playwright(venv_playwright)

    print(f"Setup complete. Virtual environment '{args.venv}' is ready to use with packages from requirements.txt.")

    sys.exit(0)