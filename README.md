# CPS 310 Final Project
## Recipe & Meal Planner

This repository contains the work in progress code for the CPS 310 final project.

The application currently supports:

- loading recipe data from JSON
- listing all recipes
- searching recipes by name
- filtering recipes by category
- viewing recipe details
- loading basic configuration from `config.json`

This is not a finished application.

### In Progress

- search by ingredient
- assign recipes to certain days of the week
- generate a grocery list
- pytest test cases for the above

## Setup

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

## Run Tests

### Windows

```powershell
python -m pytest -v
```

### macOS

```bash
python3 -m pytest -v
```
