# CPS 310 Checkpoint 1 Reflection

## Features

- search by ingredient
- assign recipes to specific days of the week
- create a grocery list

## Why Those Features?

1. Because I felt they would be the easiest to implement
2. Because I felt they were also the most interesting integratiions that make the application more useful if I were to ever use it.

## Most difficult feature

The grocery list. A recipe can appear more than once in the same plan, and each assignment has to count toward the total. The list also has to treat cup and cups as the same unit and keep a can of black beans separate from a cup of black beans. I used Decimal for quantities so amounts such as 0.1 and 0.2 add up to 0.3.

## Which GitHub Issues Represent My Planned Work 

Search by Ingredient. Issue #1
Assign Recipes to Specific Days. Issue #2
Generate a Grocery List. Issue #3

Although, I've gotten through all three at time of writing.

## Which Branch/PR Best Represents My Development Process

The feature/assign-recipes-to-days branch. I reused the recipe selection prompt, put the day validation and assignment in recipe_utils.py, and tested both the utility and the menu. I linked the PR to Issue #2 and merged it into main.

## One Meaningful Commit and It's Changes

Commit 45bb659 added the grocery list, including the menu option and the logic to total ingredients by name and unit. It also updated README.md and added tests for the totals and the menu. Keeping these changes together makes it possible to review the behavior, run its tests, and try it from the menu in the same commit.

## What Tests Were Added

- Ingredient search covers partial matches with mixed capitalization, searching ingredient names, blank searches, and recipes without ingredients.
- Meal planning covers multiple recipes on the same day, weekday order, and invalid days and recipe numbers.
- Grocery lists cover combining matching units, keeping different units separate, counting repeated assignments, and handling an empty plan. The menu test launches the app with temporary JSON files and checks the printed output.
The full suite passed 20 pytest cases, including the seven starter tests, on a clean checkout of main at ad1d981.

## One Bug or Mistake Caught During Testing

I ran python -m pytest -v in PowerShell and got No module named pytest. The error path pointed to my global Python installation. The project's .venv already had pytest installed, so I reran it with .\.venv\Scripts\python.exe -m pytest -v. All 11 ingredient-search branch tests passed on that run.

## One Improvement I Could Make

I think the ability to save the recipes assgined to days, and the grocery list would be nice. I might also want to add the ability to add ingredients and/or meals if I have additional time.

## My Plan For Remaining Work

I plan to add a Dockerfile and .dockerignore, verify that the image builds and the menu works in a container, and set up GitHub Actions to run pytest on pushes and pull requests. I will update README.md with the container commands and review what Git tracks for local files or sensitive information.
