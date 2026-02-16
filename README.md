# Pyman - Python Manager

## Features
* ♟️ Creates ready-to-work python projects
* ♟️ Setups `pytest` for you
* ♟️ Setups `vscode` for you.
* ♟️ Allows to run arbitrary scripts from `scripts` directory (For example codegen)
* ♟️ Created projects already has launchers
* ♟️ Launcher activates `venv` automatically. If `venv` is not present, it will create it

## Usage
```
USAGE:
  pyman new name  - Create new project

  pyman install   - Install dependencies
  pyman reinstall - Deletes venv and reinstalls dependencies

  pyman vscode    - (Re)Setup for vscode
  pyman pytest    - (Re)Setup pytest

  pyman run name  - Run script by name. Will run from scripts/
```


## Example
```bash
# Create new project
pyman new console_project

# Go inside
cd console_project

# Run the project as simple program
# Note: You NO NEED to activate venv, it does it automatically
./console_project
```