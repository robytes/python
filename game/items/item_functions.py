import json
import random

def load_items(file_path="C:\\Git\\python\\game\\items\\items.json"):
    with open(file_path, "r") as f:
        item_definitions = json.load(f)
    return item_definitions

def get_items(item_definitions):
    item_dictionary = load_items()
    return item_dictionary

def get_random_item(items_dictionary):
    # TODO: Add logic to filter items based on location type or other criteria if needed
    items_list = list(items_dictionary.items())
    random_item = random.choice(items_list)

    return random_item

all_items = load_items()
print("You've found a", get_random_item(all_items))