from characters.character import Character

test_scores = {
    "strength": 12,
    "intelligence": 10,
    "wisdom": 9,
    "dexterity": 14,
    "constitution": 11,
    "charisma": 8
}

test_registry = {
    "longsword": {"encumbrance_cn": 60},
    "chain_mail": {"encumbrance_cn": 300},
    "shield": {"encumbrance_cn": 100}
}

funnel_character = Character(
    name="Edric",
    ability_scores=test_scores
)

fighter = Character(
    name="Valeros",
    ability_scores=test_scores,
    character_class="fighter",
    level=1,
    inventory=["longsword", "shield"]
)
fighter.ability_scores["strength"] = 16

heavily_equipped_fighter = Character(
    name="Borin",
    ability_scores=test_scores,
    character_class="fighter",
    level=1,
    inventory=["chain_mail", "shield", "longsword"]
)
heavily_equipped_fighter.ability_scores["strength"] = 18

wizard = Character(
    name="Merlin",
    ability_scores=test_scores,
    character_class="magic_user",
    level=1
)

print(fighter.name)
print(fighter.ability_scores)
print(fighter.inventory)
print(wizard.name)
print(wizard.ability_scores)
print(wizard.inventory)
print(funnel_character.name)

assert fighter.name == "Valeros"
assert fighter.ability_scores["strength"] == 16
assert fighter.inventory == ["longsword", "shield"]
assert fighter.get_total_encumbrance(test_registry) == 160
assert fighter.get_movement_rate(test_registry) == 120

assert heavily_equipped_fighter.name == "Borin"
assert heavily_equipped_fighter.ability_scores["strength"] == 18
assert heavily_equipped_fighter.get_total_encumbrance(test_registry) == 460
assert heavily_equipped_fighter.get_movement_rate(test_registry) == 90

heavily_equipped_fighter.inventory.remove("chain_mail")
assert heavily_equipped_fighter.get_total_encumbrance(test_registry) == 160
assert heavily_equipped_fighter.get_movement_rate(test_registry) == 120

assert wizard.name == "Merlin"
assert wizard.ability_scores["strength"] == 12
assert wizard.inventory == []
assert wizard.get_total_encumbrance(test_registry) == 0
assert wizard.get_movement_rate(test_registry) == 120

assert test_scores["strength"] == 12

assert funnel_character.level == 0
assert funnel_character.character_class is None
assert funnel_character.inventory == []
assert funnel_character.get_total_encumbrance(test_registry) == 0
assert funnel_character.get_movement_rate(test_registry) == 120

print("All character tests passed!")