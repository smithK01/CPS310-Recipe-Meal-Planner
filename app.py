"""CPS 310 Recipe & Meal Planner starter application."""

from recipe_utils import (
    DAYS_OF_WEEK,
    assign_recipe_to_day,
    filter_by_category,
    generate_grocery_list,
    load_config,
    load_recipes,
    normalize_day_of_week,
    search_by_ingredient,
    search_by_name,
)


def display_recipe(recipe):
    """Display one recipe in a readable format."""
    print(f"\n{recipe['name']}")
    print("-" * len(recipe["name"]))
    print(f"Category: {recipe['category']}")
    print(f"Servings: {recipe['servings']}")
    print(f"Prep time: {recipe['prep_time']} minutes")
    print(f"Cook time: {recipe['cook_time']} minutes")
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(f"- {ingredient['quantity']} {ingredient['unit']} {ingredient['name']}")


def list_recipes(recipes):
    """Display a numbered list of recipe names."""
    if not recipes:
        print("\nNo recipes found.")
        return

    print("\nRecipes")
    print("-------")
    for index, recipe in enumerate(recipes, start=1):
        print(f"{index}. {recipe['name']} ({recipe['category']})")


def prompt_for_recipe(recipes):
    """Return the selected recipe if the user enters a valid number."""
    list_recipes(recipes)
    if not recipes:
        return

    try:
        selection = int(input("\nEnter recipe number: "))
    except ValueError:
        print("Invalid selection.")
        return

    if selection < 1 or selection > len(recipes):
        print("Invalid selection.")
        return

    return recipes[selection - 1]


def choose_recipe(recipes):
    """Prompt the user to select and view a recipe."""
    recipe = prompt_for_recipe(recipes)
    if recipe is not None:
        display_recipe(recipe)


def prompt_to_assign_recipe(recipes, meal_plan):
    """Prompt for a day and recipe to add to the weekly plan."""
    day = input("Enter a day of the week (Monday-Sunday): ")
    try:
        day = normalize_day_of_week(day)
    except ValueError as error:
        print(error)
        return

    recipe = prompt_for_recipe(recipes)
    if recipe is None:
        return

    assign_recipe_to_day(meal_plan, day, recipe)
    print(f"Assigned {recipe['name']} to {day}.")


def display_meal_plan(meal_plan):
    """Display the assigned recipes for each day of the week."""
    print("\nWeekly Meal Plan")
    print("----------------")
    for day in DAYS_OF_WEEK:
        recipe_names = ", ".join(recipe["name"] for recipe in meal_plan.get(day, []))
        print(f"{day}: {recipe_names or 'No recipes assigned'}")


def display_grocery_list(grocery_list):
    """Display the ingredient quantities needed for the weekly plan."""
    if not grocery_list:
        print("\nNo ingredients in the weekly meal plan.")
        return

    print("\nGrocery List")
    print("------------")
    for ingredient in grocery_list:
        quantity = ingredient["quantity"].normalize()
        amount = f"{quantity:f} {ingredient['unit']}".rstrip()
        print(f"- {amount} {ingredient['name']}")


def main():
    """Run the starter Recipe & Meal Planner."""
    config = load_config("config.json")
    recipes = load_recipes(config["recipe_file"])
    meal_plan = {}

    while True:
        print(f"\n{config['app_title']}")
        print("=" * len(config["app_title"]))
        print("1. List all recipes")
        print("2. Search recipes by name")
        print("3. Filter recipes by category")
        print("4. View recipe details")
        print("5. Search recipes by ingredient")
        print("6. Assign a recipe to a day")
        print("7. View weekly meal plan")
        print("8. Generate grocery list")
        print("9. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            list_recipes(recipes)
        elif choice == "2":
            term = input("Enter recipe name: ").strip()
            list_recipes(search_by_name(recipes, term))
        elif choice == "3":
            category = input("Enter category: ").strip()
            list_recipes(filter_by_category(recipes, category))
        elif choice == "4":
            choose_recipe(recipes)
        elif choice == "5":
            ingredient = input("Enter ingredient: ")
            list_recipes(search_by_ingredient(recipes, ingredient))
        elif choice == "6":
            prompt_to_assign_recipe(recipes, meal_plan)
        elif choice == "7":
            display_meal_plan(meal_plan)
        elif choice == "8":
            display_grocery_list(generate_grocery_list(meal_plan))
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-9.")


if __name__ == "__main__":
    main()
