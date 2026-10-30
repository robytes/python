# Load, combine, and validate item definitions
# Work with item definitions, such as looking up damage, weight, tags, or category.
import json
from pathlib import Path

def load_item_registry():
    registry = {}

    data_directory = Path(__file__).resolve().parent / "data"
    for item_def_file in data_directory.glob('*.json'):
        with open(item_def_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item, value in data.items():
            if item in registry:
                print(f"WARNING: Duplicate item '{item}' found in {item_def_file.name}")
                continue
            registry[item] = value
    return registry    

# For testing.
if __name__ == "__main__":
    all_items = load_item_registry()

    print(f"Loaded {len(all_items)} items")
    print(all_items["longsword"])
    print(all_items["potion_of_healing"])