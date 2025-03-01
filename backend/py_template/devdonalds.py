from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	# TODO: implement me

	# Check if recipeName is None or empty
	if recipeName is None:
		return None
	
	# Replace unwanted chars with a whitespace
	cleanRecipeName = re.sub(r'[-_]', ' ', recipeName)

	# Delete non-alpha except whitespace
	cleanRecipeName = re.sub(r'[^A-Za-z ]', '', cleanRecipeName)

	# Remove all the extra whitespaces
	# split removes trailing and leading spaces and splits string into list of 
	# words, using whitespace as seperator
	cleanRecipeName = cleanRecipeName.split()
	# join the list back into a string with a whitespace inbetween
	cleanRecipeName = " ".join(cleanRecipeName)

	# string has length > 0
	if not cleanRecipeName:
		return None

	# Capitalise first letter of each word and others lowercase
	cleanRecipeName = cleanRecipeName.title()
	
	return cleanRecipeName


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	# TODO: implement me
    data = request.get_json()

    # validate type
    entry_type = data.get('type')
    if entry_type not in ['recipe', 'ingredient']:
        return "Invalid 'type', must be 'recipe' or 'ingredient'", 400

    # validate name
    name = data.get('name')
    if not isinstance(name, str) or name.strip() == "":
        return "Invalid or missing 'name'", 400

    # check if name is unique in cookbook
    if name in cookbook:
        return "Name already exists in the cookbook", 400

    # validate requiredItems
    if entry_type == 'recipe':
        required_items_data = data.get('requiredItems')
        if not isinstance(required_items_data, list):
            return "'requiredItems' must be a list", 400

        required_items = []
        for item in required_items_data:
            if not isinstance(item, dict):
                return "Each item in 'requiredItems' must be an object", 400
            if ('name' not in item or
                'quantity' not in item or
                not isinstance(item['name'], str) or
                not isinstance(item['quantity'], int)):
                return "Invalid 'requiredItems' entry", 400

            required_items.append(
                RequiredItem(name=item['name'], quantity=item['quantity'])
            )

        # add recipe
        new_entry = Recipe(name=name, required_items=required_items)

    # ingredient
    else: 
        # validate cookTime
        cook_time = data.get('cookTime')
        if not isinstance(cook_time, int) or cook_time < 0:
            return "'cookTime' must be a non-negative integer", 400

        # create ingredient entry
        new_entry = Ingredient(name=name, cook_time=cook_time)

    # store in cookbook
    cookbook[name] = new_entry

    return "", 200

# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
