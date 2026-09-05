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
    attempted_items = set()
    while item_slots > len(location_items):
        item_name, item_definition = item_functions.get_random_item(all_items)
        if item_name in attempted_items:
            print(item_name, "already attempted")
            if item_name in location_items:
                print(item_name, "already exists in", location[0])
        elif location[0] in item_definition["locations"]:
            location_items.append(item_name)
            attempted_items.add(item_name)
            print(item_name, "assigned to", location[0])
        else:
            attempted_items.add(item_name)
            print(item_name, "not valid for", location[0])
            
        if len(all_items) == len(attempted_items) and len(location_items) < item_slots:
            print("all item assignments attempted...")
            break
    
    return location_items

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

location = get_random_location()
location_items = populate_items(location)
item_definitions = item_functions.load_items()
location_tags_count = count_location_tags(location_items, item_definitions)

print("In the", location[0], "you've found these items:")
print(location_items)