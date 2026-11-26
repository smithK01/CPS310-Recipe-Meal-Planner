"""Utility functions for the Recipe & Meal Planner."""

import json
from decimal import Decimal


DAYS_OF_WEEK = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)

_UNIT_ALIASES = {
    "cans": "can",
    "cloves": "clove",
    "cups": "cup",
    "lbs": "lb",
}


def load_config(filename):
    """Load application configuration from a JSON file."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def load_recipes(filename):
    """Load recipe data from a JSON file."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def search_by_name(recipes, search_term):
    """Return recipes whose names contain the search term."""
    search_term = search_term.lower()
    return [
        recipe
        for recipe in recipes
        if search_term in recipe["name"].lower()
    ]


def search_by_ingredient(recipes, search_term):
    """Return recipes with an ingredient name that contains the search term."""
    search_term = search_term.strip().casefold()
    if not search_term:
        return []

    return [
        recipe
        for recipe in recipes
        if any(
            search_term in ingredient["name"].casefold()
            for ingredient in recipe.get("ingredients", [])
        )
    ]


def filter_by_category(recipes, category):
    """Return recipes that match the requested category."""
    category = category.lower()
    return [
        recipe
        for recipe in recipes
        if recipe["category"].lower() == category
    ]


def normalize_day_of_week(day):
    """Return the canonical day name or raise ValueError for an invalid day."""
    day = day.strip().capitalize()
    if day not in DAYS_OF_WEEK:
        raise ValueError("Invalid day. Enter Monday through Sunday.")
    return day


def assign_recipe_to_day(meal_plan, day, recipe):
    """Append a recipe to the given day in the weekly plan."""
    day = normalize_day_of_week(day)
    meal_plan.setdefault(day, []).append(recipe)


def generate_grocery_list(meal_plan):
    """Return ingredient totals for the weekly meal plan, sorted by name and unit."""
    totals = {}
    for recipes in meal_plan.values():
        for recipe in recipes:
            for ingredient in recipe.get("ingredients", []):
                name = ingredient["name"].strip()
                unit = ingredient["unit"].strip().casefold()
                unit = _UNIT_ALIASES.get(unit, unit)
                key = (name.casefold(), unit)
                item = totals.setdefault(
                    key,
                    {"name": name, "quantity": Decimal(0), "unit": unit},
                )
                item["quantity"] += Decimal(str(ingredient["quantity"]))

    return [totals[key] for key in sorted(totals)]
