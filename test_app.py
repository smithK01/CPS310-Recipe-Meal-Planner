"""Tests for weekly meal planning in the recipe app."""

import app


def test_main_assigns_recipes_and_displays_weekly_plan(monkeypatch, capsys):
    recipes = [
        {"name": "Tomato Pasta", "category": "Dinner"},
        {"name": "Veggie Omelet", "category": "Breakfast"},
    ]
    config = {"app_title": "Test Planner", "recipe_file": "recipes.json"}
    monkeypatch.setattr(app, "load_config", lambda _: config)
    monkeypatch.setattr(app, "load_recipes", lambda _: recipes)
    answers = iter(("6", "Sunday", "1", "6", " monday ", "2", "6", "MONDAY", "1", "7", "8"))
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    app.main()

    output = capsys.readouterr().out
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


def test_prompt_to_assign_recipe_rejects_invalid_selections(monkeypatch, capsys):
    recipes = [{"name": "Tomato Pasta", "category": "Dinner"}]
    meal_plan = {}
    answers = iter(("Funday", "Monday", "0"))
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    app.prompt_to_assign_recipe(recipes, meal_plan)
    app.prompt_to_assign_recipe(recipes, meal_plan)

    assert meal_plan == {}
    output = capsys.readouterr().out
    assert "Invalid day." in output
    assert "Invalid selection." in output
