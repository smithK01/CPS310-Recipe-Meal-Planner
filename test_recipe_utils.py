"""Tests for the Recipe & Meal Planner."""

import json
from decimal import Decimal

import pytest

from recipe_utils import (
    assign_recipe_to_day,
    filter_by_category,
    generate_grocery_list,
    load_config,
    load_recipes,
    search_by_ingredient,
    search_by_name,
)


def test_search_by_name_finds_partial_match():
    recipes = [
        {"name": "Chicken Alfredo", "category": "Dinner"},
        {"name": "Berry Smoothie", "category": "Snack"},
    ]
    result = search_by_name(recipes, "chicken")
    assert result == [{"name": "Chicken Alfredo", "category": "Dinner"}]


def test_search_by_name_is_case_insensitive():
    recipes = [
        {"name": "Chicken Alfredo", "category": "Dinner"},
        {"name": "Berry Smoothie", "category": "Snack"},
    ]
    result = search_by_name(recipes, "SMOOTHIE")
    assert result == [{"name": "Berry Smoothie", "category": "Snack"}]


def test_search_by_name_returns_empty_list_when_no_match():
    recipes = [{"name": "Chicken Alfredo", "category": "Dinner"}]
    assert search_by_name(recipes, "pizza") == []


def test_search_by_ingredient_finds_partial_matches_case_insensitively():
    recipes = [
        {
            "name": "Cheese Omelet",
            "ingredients": [{"name": "Cheddar cheese"}, {"name": "parmesan cheese"}],
        },
        {"name": "Berry Smoothie", "ingredients": [{"name": "berries"}]},
        {"name": "Tomato Pasta", "ingredients": [{"name": "parmesan cheese"}]},
    ]
    assert search_by_ingredient(recipes, "  ChEeSe  ") == [recipes[0], recipes[2]]


def test_search_by_ingredient_ignores_recipe_names_and_units():
    recipes = [
        {
            "name": "Yogurt Cups",
            "ingredients": [{"name": "greek yogurt", "quantity": 1, "unit": "cup"}],
        }
    ]
    assert search_by_ingredient(recipes, "cup") == []


def test_search_by_ingredient_skips_recipes_without_ingredients():
    recipes = [{"name": "Fruit Salad", "ingredients": []}, {"name": "Toast"}]
    assert search_by_ingredient(recipes, "bread") == []


def test_search_by_ingredient_returns_empty_list_for_blank_term():
    recipes = [{"name": "Berry Smoothie", "ingredients": [{"name": "berries"}]}]
    assert search_by_ingredient(recipes, "  ") == []


def test_filter_by_category_returns_matching_recipes():
    recipes = [
        {"name": "Chicken Alfredo", "category": "Dinner"},
        {"name": "Berry Smoothie", "category": "Snack"},
        {"name": "Tomato Pasta", "category": "Dinner"},
    ]
    result = filter_by_category(recipes, "Dinner")
    assert result == [
        {"name": "Chicken Alfredo", "category": "Dinner"},
        {"name": "Tomato Pasta", "category": "Dinner"},
    ]


def test_filter_by_category_is_case_insensitive():
    recipes = [{"name": "Chicken Alfredo", "category": "Dinner"}]
    assert filter_by_category(recipes, "dinner") == [
        {"name": "Chicken Alfredo", "category": "Dinner"}
    ]


def test_load_config_reads_json(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(
        json.dumps(
            {
                "app_title": "Test Planner",
                "recipe_file": "recipes.json",
                "default_servings": 2,
            }
        ),
        encoding="utf-8",
    )
    result = load_config(config_file)
    assert result["app_title"] == "Test Planner"
    assert result["default_servings"] == 2


def test_load_recipes_reads_json(tmp_path):
    recipe_file = tmp_path / "recipes.json"
    sample = [
        {
            "name": "Test Recipe",
            "category": "Lunch",
            "servings": 2,
            "prep_time": 5,
            "cook_time": 10,
            "ingredients": [],
        }
    ]
    recipe_file.write_text(json.dumps(sample), encoding="utf-8")
    assert load_recipes(recipe_file) == sample


def test_assign_recipe_to_day_appends_to_normalized_day():
    omelet = {"name": "Veggie Omelet"}
    pasta = {"name": "Tomato Pasta"}
    meal_plan = {"Monday": [omelet]}

    assign_recipe_to_day(meal_plan, "  MONDAY  ", pasta)

    assert meal_plan == {"Monday": [omelet, pasta]}


def test_assign_recipe_to_day_rejects_invalid_day():
    meal_plan = {}

    with pytest.raises(ValueError, match="Invalid day"):
        assign_recipe_to_day(meal_plan, "Funday", {"name": "Tomato Pasta"})

    assert meal_plan == {}


def test_generate_grocery_list_totals_ingredients_by_name_and_unit():
    taco_bowls = {
        "ingredients": [
            {"name": "black beans", "quantity": 1, "unit": "can"},
            {"name": "salsa", "quantity": 0.1, "unit": "cups"},
        ]
    }
    quesadillas = {
        "ingredients": [
            {"name": "Black Beans", "quantity": 1, "unit": "cup"},
            {"name": " SALSA ", "quantity": 0.2, "unit": " CUP "},
        ]
    }
    meal_plan = {"Monday": [taco_bowls], "Thursday": [quesadillas]}

    assert generate_grocery_list(meal_plan) == [
        {"name": "black beans", "quantity": 1, "unit": "can"},
        {"name": "Black Beans", "quantity": 1, "unit": "cup"},
        {"name": "salsa", "quantity": Decimal("0.3"), "unit": "cup"},
    ]


def test_generate_grocery_list_counts_each_assignment():
    recipe = {"ingredients": [{"name": "basil", "quantity": 0.25, "unit": "cup"}]}
    meal_plan = {"Monday": [recipe, recipe], "Friday": [recipe]}

    assert generate_grocery_list(meal_plan) == [
        {"name": "basil", "quantity": Decimal("0.75"), "unit": "cup"},
    ]
    assert recipe["ingredients"][0]["quantity"] == 0.25


@pytest.mark.parametrize("meal_plan", [{}, {"Monday": [{"ingredients": []}]}])
def test_generate_grocery_list_returns_empty_list_without_ingredients(meal_plan):
    assert generate_grocery_list(meal_plan) == []
