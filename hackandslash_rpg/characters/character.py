class Character:
    def __init__(self, name, inventory=None):
        self.name = name
        self.inventory = list(inventory) if inventory is not None else []