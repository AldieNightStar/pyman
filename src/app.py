import os
import sys
import project

def main(args):
    if len(args) < 1:
        print("USAGE:")
        print("  pyman new name  - Create new project")
        print("")
        print("  pyman install   - Install dependencies")
        print("  pyman reinstall - Deletes venv and reinstalls dependencies")
        print("  pyman pack      - Creates wheel build package from project")
        print("")
        print("  pyman vscode    - (Re)Setup for vscode")
        print("  pyman pytest    - (Re)Setup pytest")
        print("")
        print("  pyman run name  - Run script by name. Will run from scripts/")
        return
    execute(args[0], args[1:])

def execute(cmd, args):
    root = os.path.abspath("./")
    if cmd == "new":
        if len(args) < 1:
            print("--- Enter name of the project")
            return
        name = args[0]
        if name in ("src", "test", "tests", "new", "scripts") or len(name) < 3:
            print("--- Incorrect name for the project")
            return
        project.create_project("./" + name, name)
    elif cmd == "install":
        if not project.is_in_project(root):
            print("--- Please, run this command from inside of the project")
            return
        project.install_requirements(root)
    elif cmd == "reinstall":
        if not project.is_in_project(root):
            print("--- Please, run this command from inside of the project")
            return
        project.remove_venv(root)
        project.create_venv(root)
        project.install_requirements(root)
    elif cmd == "vscode":
        if not project.is_in_project(root):
            print("--- Please, run this command from inside of the project")
            return
        project.setup_vscode(root)
    elif cmd == "pytest":
        if not project.is_in_project(root):
            print("--- Please, run this command from inside of the project")
            return
        project.setup_pytest(root)
    elif cmd == "run":
        if len(args) < 1:
            print("Enter name of the script and args for that script")
            return
        project.run_script(root, args[0], args[1:])
    elif cmd == "pack":
        project.pack(root)

if __name__ == "__main__":
    main(sys.argv[1:])
