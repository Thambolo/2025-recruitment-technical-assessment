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
cookbook = None

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
	return 'not implemented', 500


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
