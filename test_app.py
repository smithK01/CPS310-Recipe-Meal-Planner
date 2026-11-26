"""Tests for the recipe app's command-line menus."""

import json
import subprocess
import sys
from pathlib import Path


def run_app(tmp_path, recipes, answers):
    config = {"app_title": "Test Planner", "recipe_file": "recipes.json"}
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config), encoding="utf-8")
    recipe_file = tmp_path / "recipes.json"
    recipe_file.write_text(json.dumps(recipes), encoding="utf-8")

    app_file = Path(__file__).resolve().with_name("app.py")
    result = subprocess.run(
        [sys.executable, str(app_file)],
        cwd=tmp_path,
        input="\n".join(answers) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_main_assigns_recipes_and_displays_weekly_plan(tmp_path):
    recipes = [
        {"name": "Tomato Pasta", "category": "Dinner"},
        {"name": "Veggie Omelet", "category": "Breakfast"},
    ]
    answers = ["6", "Sunday", "1", "6", " monday ", "2", "6", "MONDAY", "1", "7", "9"]

    output = run_app(tmp_path, recipes, answers)

    assert "Assigned Veggie Omelet to Monday." in output
    assert (
        "Weekly Meal Plan\n"
        "----------------\n"
        "Monday: Veggie Omelet, Tomato Pasta\n"
        "Tuesday: No recipes assigned\n"
        "Wednesday: No recipes assigned\n"
        "Thursday: No recipes assigned\n"
        "Friday: No recipes assigned\n"
        "Saturday: No recipes assigned\n"
        "Sunday: Tomato Pasta\n"
    ) in output


def test_main_rejects_invalid_day_and_recipe_selections(tmp_path):
    recipes = [{"name": "Tomato Pasta", "category": "Dinner"}]
    answers = ["6", "Funday", "6", "Monday", "0", "7", "9"]

    output = run_app(tmp_path, recipes, answers)

    assert "Invalid day." in output
    assert "Invalid selection." in output
    assert "Monday: No recipes assigned" in output
    assert "Assigned " not in output


def test_main_generates_grocery_list_from_assigned_recipes(tmp_path):
    recipes = [
        {
            "name": "Oatmeal",
            "category": "Breakfast",
            "ingredients": [{"name": "oats", "quantity": 0.5, "unit": "cup"}],
        },
        {
            "name": "Veggie Omelet",
            "category": "Breakfast",
            "ingredients": [{"name": "eggs", "quantity": 3, "unit": "whole"}],
        },
    ]
    answers = ["8", "6", "Wednesday", "1", "8", "9"]

    output = run_app(tmp_path, recipes, answers)

    assert "No ingredients in the weekly meal plan." in output
    assert "Grocery List\n------------\n- 0.5 cup oats\n" in output
    assert "eggs" not in output
