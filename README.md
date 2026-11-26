# CPS 310 Final Project
## Recipe & Meal Planner

This repository contains the work in progress code for the CPS 310 final project.

The application currently supports:

- loading recipe data from JSON
- listing all recipes
- searching recipes by name
- searching recipes by ingredient (case-insensitive partial matches)
- filtering recipes by category
- viewing recipe details
- assigning multiple recipes to each day and viewing the weekly meal plan during the current session
- generating a grocery list with ingredient totals from the weekly meal plan
- loading basic configuration from `config.json`

This is not a finished application.

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
