from copy import deepcopy
from items.inventory import calculate_total_encumbrance, get_encumbrance_status

class Character:
    def __init__(
            self,
            name,
            ability_scores,
            character_class=None,
            level=0,
            inventory=None,
            equipped_items=None
    ):
        self.name = name
        self.character_class = character_class
        self.level = level
        self.ability_scores = dict(ability_scores)
        self.inventory = list(inventory) if inventory is not None else []
        self.equipped_items = (
            deepcopy(equipped_items)
            if equipped_items is not None
            else {
                "weapons": {
                    "main_hand": None,
                    "off_hand": None
                },
                "armor": {
                    "body": None,
                    "shield": None
                },
                "misc_magic_items": {
                    "head": None,
                    "neck": None,
                    "cloak": None,
                    "wrists": None,
                    "hands": None,
                    "waist": None,
                    "feet": None,
                    "ring_left": None,
                    "ring_right": None
                }
            }
        )

    def get_total_encumbrance(self, item_registry):
        total_encumbrance = calculate_total_encumbrance(self.inventory, item_registry)
        return total_encumbrance

    def get_movement_rate(self, item_registry):
        encumbrance_status = get_encumbrance_status(
            self.get_total_encumbrance(item_registry)
            )
        return encumbrance_status["movement_rate"]

#    def add_item(self, item_name, item_registry):
        
