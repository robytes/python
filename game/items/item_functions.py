import json
import random

rarity_weights = {
    "common": 50,
    "uncommon": 30,
    "rare": 15,
    "very rare": 4,
    "exceptional": 1
}

def load_items(file_path="C:\\Git\\python\\game\\items\\items.json"):
    with open(file_path, "r") as f:
        item_definitions = json.load(f)
    return item_definitions

def get_items(item_definitions):
    item_dictionary = load_items()
    return item_dictionary

def get_random_item(items_dictionary):
    items_list = list(items_dictionary.items())
    random_item = random.choice(items_list)

    return random_item

def get_weighted_random_item(eligible_items, all_items):
    if not eligible_items:
        print("No eligible items to choose from...")
        return None

    eligible_items_weight = {}
    total_weight = 0
    accumulated_weight = 0
    for eligible_item in eligible_items:
        item_definition = all_items[eligible_item]
        item_rarity = item_definition["rarity"]
        item_rarity_weight = rarity_weights[item_rarity]
        eligible_items_weight[eligible_item] = item_rarity_weight 
        total_weight += item_rarity_weight
    
    random_roll = random.randint(1, total_weight)
    for item_name, item_weight in eligible_items_weight.items():
        accumulated_weight += item_weight 
        if random_roll <= accumulated_weight:             
            return item_name 

all_items = load_items()
print("You've found a", get_random_item(all_items))