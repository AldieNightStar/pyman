from multiprocessing.util import is_exiting
from typing import cast
import subprocess
import os.path
import shutil
import files
import venv
import os

__APP_PATHS = ["src", "test"]

def is_in_project(root):
    src_dir = os.path.join(root, "src")
    test_dir = os.path.join(root, "test")

    return os.path.exists(src_dir) and os.path.exists(test_dir)

def create_project(root, project_name):
    if os.path.exists(root):
       print(f"--- Can't create new project here: {root}")
       return

    src_dir = os.path.join(root, "src")
    test_dir = os.path.join(root, "test")
    
    # Make dirs
    files.makedir(src_dir)
    files.makedir(test_dir)

    # Copy .gitignore
    shutil.copy(
        os.path.join(files.ROOT_DIR, ".gitignore"),
        os.path.join(root, ".gitignore"),
    )

    # Create basic test
    files.write_file(os.path.join(test_dir, "test_basic.py"), [
        "def test_app_has_main():",
        "    from app import main",
        "    assert main is not None"
    ])

    # Create basic app file
    files.write_file(os.path.join(src_dir, "app.py"), [
        "def main(args):",
        "    print(\"Works!\")",
        "",
        "if __name__ == \"__main__\":",
        "    import sys",
        "    main(sys.argv[1:])",
        ""
    ])

    # Create pytest config
    setup_pytest(root)

    # Setup vscode
    setup_vscode(root)
    
    # Copy launcher
    shutil.copy(
        os.path.join(files.ROOT_DIR, "pyman"),
        os.path.join(root, project_name),
    )

    # Create pyproject.toml
    create_pyproject(root, project_name)

    # Create venv
    create_venv(root)

    # Setup scripts
    setup_scripts(root)

    # Create git
    files.init_git_repo(root)

def setup_pytest(root):
    pytest_file = os.path.join(root, "pytest.ini")
    files.write_file(pytest_file, [
         "[pytest]",
         f"pythonpath = . {' '.join(__APP_PATHS)}",
         "testpaths = test",
         "python_files = test_*.py",
    ])

def setup_vscode(root):
    vscode_dir = os.path.join(root, ".vscode")
    settings_file = os.path.join(vscode_dir, "settings.json")

    # Ensure .vscode directory exists
    if not os.path.exists(vscode_dir): os.makedirs(vscode_dir)

    vscode_paths = ["${workspaceFolder}"]
    for path in __APP_PATHS:
        vscode_paths.append("${workspaceFolder}/" + str(path))
    
    # Cross-platform separator for PYTHONPATH
    python_path_str = os.pathsep.join(vscode_paths)

    # Update settings dictionary
    files.update_json(settings_file, {
        "python.analysis.extraPaths": vscode_paths,
        "python.analysis.autoImportCompletions": True,

        # --- Pytest Integration ---
        "python.testing.pytestEnabled": True,
        "python.testing.unittestEnabled": False,
        "python.testing.pytestArgs": [
            "test",
            "-v"
        ],

        # Set terminal environment so 'python' in the internal terminal sees the paths
        "terminal.integrated.env.linux": {"PYTHONPATH": python_path_str},
        "terminal.integrated.env.osx": {"PYTHONPATH": python_path_str},
        "terminal.integrated.env.windows": {"PYTHONPATH": python_path_str}
    })
    
    print(f"--- VS Code configuration updated in {settings_file}")

def create_venv(root):
    venv_dir = os.path.join(root, "venv")
    venv.create(venv_dir, with_pip=True)
    install_requirements(root)

def install_requirements(root):
    venv_dir = os.path.join(root, "venv")
    pip_exe = _venv_get_pip(venv_dir)
    subprocess.check_call([pip_exe, "install", "."], cwd=root)

def remove_venv(root):
    venv_dir = os.path.join(root, "venv")
    if os.path.exists(venv_dir):
        shutil.rmtree(venv_dir)

def _venv_get_pip(venv_dir):
    if os.name == "nt":
        return os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_dir, "bin", "pip")

def create_pyproject(root, name):
    pyproject_file = os.path.join(root, "pyproject.toml")
    pyproject_template = files.read_res("pyproject.toml")

    if pyproject_file is None:
        return

    files.write_file(pyproject_file, cast(str, pyproject_template)\
        .replace("%NAME%", name)
    )

def setup_scripts(root):
    scripts_dir = os.path.join(root, "scripts")
    sample_script_file = os.path.join(scripts_dir, "hello.py")

    files.makedir(scripts_dir)
    files.write_file(sample_script_file, "print(\"Hello from Scripts\")\n")

def run_script(root, name, args):
    os.environ["PYTHONPATH"] = get_pythonpath(root)
    files.run_python(root, f"scripts.{name}", args, cwd=root)

def get_pythonpath(root):
    paths = [root]
    for path in __APP_PATHS:
        paths.append(os.path.join(root, path))
    return os.pathsep.join(paths)