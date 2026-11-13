# Add, remove, search, and count inventory items
# Work with collections of items, such as adding a sword to a character's inventory or finding all wooden items they possess.
from .registry import load_item_registry

def count_items_by_tag(item_registry):
    tag_counts = {}

    for item_name, item_data in item_registry.items():
        tags = item_data["tags"]
        for tag in tags:
            if tag in tag_counts:
                tag_counts[tag] += 1
            else:
                tag_counts[tag] = 1
    
    return tag_counts

def find_most_common_tags(tag_counts):
    most_common_tags = {}
    highest_count = 0

    for tag, count in tag_counts.items():
        if count > highest_count:
            highest_count = count
            most_common_tags = {tag: count}
        elif count == highest_count:
            most_common_tags[tag] = count
    
    return most_common_tags

def find_top_three_tags(tag_counts):
    top_three = []

    for tag, count in tag_counts.items():
        tag_added = False
        for i in range(len(top_three)):
            if count > top_three[i][1]:
                top_three.insert(i, (tag, count))
                tag_added = True
                break

        if len(top_three) < 3 and not tag_added:
            top_three.append((tag, count))

        if len(top_three) > 3:
            top_three.pop()

    return top_three

def calculate_total_encumbrance(inventory, item_registry):
    total_encumbrance = 0
    for item in inventory:
        weight = item_registry[item]["encumbrance_cn"]
        total_encumbrance += weight
    return total_encumbrance

def get_encumbrance_status(total_encumbrance):    
    encumbrance_status = {
        "category": "",
        "movement_rate": 0
    }
    if total_encumbrance <= 400:
        encumbrance_status["category"] = "unencumbered"
        encumbrance_status["movement_rate"] = 120
    elif total_encumbrance <= 800:
        encumbrance_status["category"] = "light"
        encumbrance_status["movement_rate"] = 90
    elif total_encumbrance <= 1200:
        encumbrance_status["category"] = "moderate"
        encumbrance_status["movement_rate"] = 60
    elif total_encumbrance <= 1600:
        encumbrance_status["category"] = "heavy"
        encumbrance_status["movement_rate"] = 30
    elif total_encumbrance <= 2400:
        encumbrance_status["category"] = "severe"
        encumbrance_status["movement_rate"] = 15
    else:
        encumbrance_status["category"] = "immobile"
        encumbrance_status["movement_rate"] = 0
    return encumbrance_status