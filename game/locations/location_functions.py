import json
import random
from items import item_functions

def load_locations(file_path="C:\\Git\\python\\game\\locations\\locations.json"):
    with open(file_path, "r") as f:
        location_definitions = json.load(f)
    return location_definitions

def get_random_location():
    locations_dictionary = load_locations()
    locations_list = list(locations_dictionary.items())
    random_location = random.choice(locations_list)
    return random_location

def populate_items(location):
    all_items = item_functions.load_items()
    item_slots = location[1]["item_slots"]
    location_items = location[1]["items"]

    eligible_items = []
    for item_name, item_definition in all_items.items():
        if location[0] in item_definition["locations"] and item_name not in location_items:
            eligible_items.append(item_name)
    
    while item_slots > len(location_items):
        # random_item_name = random.choice(eligible_items)
        random_weighted_item = item_functions.get_weighted_random_item(eligible_items, all_items)
        location_items.append(random_weighted_item)
        eligible_items.remove(random_weighted_item)
        print(random_weighted_item, "assigned to", location[0])

            
        if len(eligible_items) == 0 and len(location_items) < item_slots:
            print("all eligible items assigned...")
            break

    return location_items

#TODO: Was a practice exercise. Can probably remove.
def count_location_tags(location_items, item_definitions):
    tags_count = {}
    for item in location_items:
        tags = item_definitions[item]["tags"]
        for tag in tags:
            if tag in tags_count:
                tags_count[tag] += 1
            else:
                tags_count[tag] = 1
    return tags_count

def summarize_location_loot(location_items, all_items):
    location_loot = {
        "total_gp": 0,
        "weapons": [],
        "armor": [],
        "consumables": [],
        "limited_use_items": []
    }

    for location_item in location_items:
        item_definition= all_items[location_item]
        
        location_loot["total_gp"] += item_definition["gp_value"]
        if "weapon" in item_definition["tags"]:
            location_loot["weapons"].append(location_item)
        if "armor" in item_definition["tags"]:
            location_loot["armor"].append(location_item)
        if "consumable" in item_definition["tags"]:
            location_loot["consumables"].append(location_item)
        if item_definition["uses"] is not None:
            location_loot["limited_use_items"].append(location_item) 
    
    return location_loot

def analyze_location_loot(location_items, all_items):
    location_loot = {
        "total_gp": 0,
        "items_by_rarity": {},
        "tag_counts": {},
        "limited_use_items": []
    }

    for location_item in location_items:
        item_definition = all_items[location_item]
        
        location_loot["total_gp"] += item_definition["gp_value"]
        item_rarity = item_definition["rarity"]
        if item_rarity not in location_loot["items_by_rarity"]:
            location_loot["items_by_rarity"][item_rarity] = [location_item]
        else:
            location_loot["items_by_rarity"][item_rarity].append(location_item)

        for tag in item_definition["tags"]:
            if tag not in location_loot["tag_counts"]:
                location_loot["tag_counts"][tag] = 1
            else:
                location_loot["tag_counts"][tag] += 1

        if item_definition["uses"] is not None:
            location_loot["limited_use_items"].append(location_item)
    return location_loot

def location_rarity_summary(location_items, all_items):
    rarity_summary = {}
    for thing in location_items:
        item_definition = all_items[thing]
        if item_definition["rarity"] not in rarity_summary:
            rarity_summary[item_definition["rarity"]] = 1
        else:
            rarity_summary[item_definition["rarity"]] += 1
    
    return rarity_summary

def get_unique_location_tags(location_items, all_items):
    unique_tags= set()
    for thing in location_items:
        item_definition = all_items[thing]
        for tag in item_definition["tags"]:
            if tag not in unique_tags:
                unique_tags.add(tag)

    return unique_tags

def get_valuable_items(location_items, all_items, minimum_gp):
    valuable_items = []
    for thing in location_items:
        thing_value = all_items[thing]["gp_value"]
        if thing_value >= minimum_gp:
            valuable_items.append(thing)
    return valuable_items


location = get_random_location()
location_items = populate_items(location)
item_definitions = item_functions.load_items()
location_tags_count = count_location_tags(location_items, item_definitions)


print("In the", location[0], "you've found these items:")
print(location_items)