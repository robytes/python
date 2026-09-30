from items import item_functions

class Location:
    def __init__(self, location_type, item_slots):
        self.location_type = location_type
        self.item_slots = item_slots
        self.items = set()
        
    item_definitions = item_functions.load_items("items/items.json")


