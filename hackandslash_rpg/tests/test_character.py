from characters.character import Character

fighter = Character("Valeros", ["longsword", "shield"])
wizard = Character("Merlin")

print(fighter.name)
print(fighter.inventory)
print(wizard.name)
print(wizard.inventory)

assert fighter.name == "Valeros"
assert fighter.inventory == ["longsword", "shield"]
assert wizard.name == "Merlin"
assert wizard.inventory == []

print("All character tests passed!")