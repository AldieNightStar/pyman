import json
import os
import subprocess

ROOT_DIR = os.path.dirname(
    os.path.abspath(os.path.join(__file__, ".."))
)

def write_file(name, src):
    if type(src) is list:
        src = "\n".join(src)
    with open(name, 'w') as f:
        f.write(src)

def write_json(name, value):
    with open(name, 'w') as f:
        json.dump(value, f, indent=4)
    
def read_json(name) -> dict:
    if not os.path.exists(name): return {}
    with open(name, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def makedir(name):
    try:
        os.makedirs(name)
    except FileExistsError:
        pass

def update_json(name, updates):
    value = read_json(name)
    value.update(updates)
    write_json(name, value)

def init_git_repo(root):
    try:
        subprocess.run(["git", "init"], cwd=root)
        subprocess.run(["git", "add", "."], cwd=root)
        subprocess.run(["git", "commit", "-m", "Init"], cwd=root)
    except:
        print(f"--- Wasn't able to create git repo: {root}")

def run_python(root, module, args=[], cwd="."):
    venv_dir = os.path.join(root, "venv")
    python_exe = os.path.join(venv_dir, "bin", "python") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "python.exe")
    subprocess.run([python_exe, '-m', module] + args, cwd=cwd)