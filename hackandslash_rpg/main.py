from shared.dice import roll
from copy import deepcopy

character = {
    "Conan": {
        "name": "Conan the Barbarian",
        "type": "character",
        "ability_scores": {
            "strength": {
                "score": 0,
                "modifier": 0
            },
            "intelligence": {
                "score": 0,
                "modifier": 0
            },
            "wisdom": {
                "score": 0,
                "modifier": 0
            },
            "dexterity": {
                "score": 0,
                "modifier": 0
            },
            "constitution": {
                "score": 0,
                "modifier": 0
            },
            "charisma": {
                "score": 0,
                "modifier": 0
            }
        },
        "combat_modifiers": {
            "hit_modifier": 0,
            "damage_modifier": 0,
            "initiative_modifier": 0
        },
        "combat_adjustments": {
            "hit_modifier": {},
            "damage_modifier": {},
            "defense_modifier": {},
            "initiative_modifier": {}
        },
        "hit_points": {
            "hp_max": 8,
            "hp_current": 8
        },
        "class": {
            "name": "fighter",
            "level": 1
        },
        "equipped_items": {
            "weapons": {
                "main_hand": "masterwork_longsword",
                "off_hand": None
            },
            "armor": {
                "body": "scale_mail",
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
        },
        "inventory": {}
    }
    
}

weapons = {
    "masterwork_longsword": {
        "hit_modifier": 1,
        "damage_modifier": 0,
        "damage": "d8"
    },
    "longsword": {
        "hit_modifier": 0,
        "damage_modifier": 0,
        "damage": "d8"
    },
    "shortsword": {
        "hit_modifier": 0,
        "damage_modifier": 0,
        "damage": "d6"
    }    
}

armor = {
    "leather_armor": {
        "name": "Leather Armor",
        "armor_class": 13,
        "weight": 20
    },
    "scale_mail": {
        "name": "Scale Mail",
        "armor_class": 14,
        "weight": 30
    },
    "chain_mail": {
        "name": "Chain Mail",
        "armor_class": 15,
        "weight": 40
    },
    "banded_mail": {
        "name": "Banded Mail",
        "armor_class": 16,
        "weight": 45
    },
    "plate_mail": {
        "name": "Plate Mail",
        "armor_class": 17,
        "weight": 50
    },
    "suit_armor": {
        "name": "Suit Armor",
        "armor_class": 20,
        "weight": 75
    },
    "shield": {
        "name": "Shield",
        "armor_class_bonus": 1,
        "weight": 10
    }
}

enemies = {
    "goblin": {
        "name": "goblin",
        "type": "monstrous humanoid",
        "armor_class": {
            "base_ac": 13, 
            "shield_bonus": 0
        },
        "hit_dice": "d8",
        "hit_points": {
            "hp_max": 6,
            "hp_current": 6
        },
        "combat_modifiers": {
            "hit_modifier": 0,
            "damage_modifier": 0,
            "initiative_modifier": 0
        },
        "combat_adjustments": {
            "hit_modifier": {},
            "damage_modifier": {},
            "defense_modifier": {},
            "initiative_modifier": {}
        },
        "attacks": "1",
        "damage": "weapon",
        "equipped_items": {
            "weapons": {
                "main_hand": "shortsword",
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
        },
        "inventory": {}
    },
    "orc": {
        "name": "orc",
        "type": "monstrous humanoid",
        "armor_class": {
            "base_ac": 14,
            "shield_bonus": 0
        },
        "hit_dice": "d8",
        "hit_points": {
            "hp_max": 8,
            "hp_current": 8
        },
        "combat_modifiers": {
            "hit_modifier": 1,
            "damage_modifier": 1,
            "initiative_modifier": 0
        },
        "combat_adjustments": {
            "hit_modifier": {},
            "damage_modifier": {},
            "defense_modifier": {},
            "initiative_modifier": {}
        },
        "attacks": "1",
        "damage": "weapon",
        "equipped_items": {
            "weapons": {
                "main_hand": "longsword",
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
        },
        "inventory": {}
    }
}

# Character functions
def get_ability_score_modifier(ability_score):

    if ability_score <= 8:
        ability_modifier = -1
    elif ability_score <= 12:
        ability_modifier = 0
    elif ability_score <= 15:
        ability_modifier = 1
    elif ability_score <= 17:
        ability_modifier = 2
    else:
        ability_modifier = 3
    return ability_modifier

def roll_character_ability_scores(character):
    for ability in character["ability_scores"]:
        character["ability_scores"][ability]["score"] = roll("3d6")
        character["ability_scores"][ability]["modifier"] = get_ability_score_modifier(character["ability_scores"][ability]["score"])
    
    return character["ability_scores"]

# Refactor to set base combat modifiers based on class/level and ability score modifiers.
def calculate_combat_modifiers(character, weapon, adjustments=None):
    if adjustments is None:
        adjustments = {}

    character["combat_modifiers"]["hit_modifier"] = (
        sum(adjustments.get("hit_modifier", [])) 
        + weapon.get("hit_modifier", 0)
        + character["ability_scores"]["strength"]["modifier"]
    )
    character["combat_modifiers"]["damage_modifier"] = (
        sum(adjustments.get("damage_modifier", [])) 
        + weapon.get("damage_modifier", 0)
        + character["ability_scores"]["strength"]["modifier"]
    )
    character["combat_modifiers"]["initiative_modifier"] = (
        sum(adjustments.get("initiative_modifier", []))
        + weapon.get("initiative_modifier", 0)
        + character["ability_scores"]["dexterity"]["modifier"]
    )

    return character["combat_modifiers"]



def calculate_hit_points(character):
    hp_max = character["hit_points"]["hp_max"] + character["ability_scores"]["constitution"]["modifier"]
    # if character["class"]["level"] == 1: Add in character max hp logic based on character
    # would be similar splitting operation for the dicer roller, just use the second element as max hp
    character["hit_points"]["hp_max"] = hp_max
    character["hit_points"]["hp_current"] = hp_max
    # TODO: change this to have different logic for 1st level hp (max hp + con) vs. level-up hp (d8 + con)
    return hp_max

# combat functions
def calculate_adjustments(adjustments=None):
    if adjustments is None:
        adjustments = {}

    adjustment_data = {
        "adjustment_total": 0,
        "adjustments": {}
    }
    for adjustment_name, adjustment_value in adjustments.items():
        adjustment_data["adjustments"][adjustment_name] = adjustment_value
        adjustment_data["adjustment_total"] += adjustment_value

    return adjustment_data

def calculate_attack_modifiers(combatant, weapon, attack_modifier_adjustments):
    attack_modifier = (
        attack_modifier_adjustments["adjustment_total"]
        + weapon["hit_modifier"]
        + combatant["combat_modifiers"]["hit_modifier"]
    )

    attack_modifier_data = {
        "total_hit_modifier": attack_modifier,
        "base_hit_modifier": combatant["combat_modifiers"]["hit_modifier"],
        "weapon_hit_modifier": weapon["hit_modifier"],
        "adjustment_total": attack_modifier_adjustments["adjustment_total"],
        "adjustments": attack_modifier_adjustments["adjustments"]
    }
    
    return attack_modifier_data

def calculate_damage_modifiers(combatant, weapon, damage_modifier_adjustments):
    damage_modifier = (
        damage_modifier_adjustments["adjustment_total"]
        + weapon["damage_modifier"]
        + combatant["combat_modifiers"]["damage_modifier"]
    )

    damage_modifier_data = {
        "total_damage_modifier": damage_modifier,
        "base_damage_modifier": combatant["combat_modifiers"]["damage_modifier"],
        "weapon_damage_modifier": weapon["damage_modifier"],
        "adjustment_total": damage_modifier_adjustments["adjustment_total"],
        "adjustments": damage_modifier_adjustments["adjustments"]
    }

    return damage_modifier_data

def calculate_modified_ac(equipped_armor, defense_modifier_adjustments):
    #Establishing unarmored base
    if equipped_armor["body"] is None:
        base_ac = 11
    else:
        base_ac = equipped_armor["body"]["armor_class"]

    if equipped_armor["shield"] is None:
        shield_bonus = 0
    else:
        shield_bonus = equipped_armor["shield"]["armor_class_bonus"]

    modified_ac = (
        base_ac
        + shield_bonus
        + defense_modifier_adjustments["adjustment_total"]
    )

    modified_ac_data = {
        "modified_ac": modified_ac,
        "total_bonus": shield_bonus + defense_modifier_adjustments["adjustment_total"],
        "base_ac": base_ac,
        "shield_bonus": shield_bonus,
        "adjustment_total": defense_modifier_adjustments["adjustment_total"],
        "adjustments": defense_modifier_adjustments["adjustments"]
    }

    return modified_ac_data

def calculate_initiative_modifiers(combatant, weapon, initiative_modifier_adjustments):
    weapon_initiative_modifier = weapon.get("initiative_modifier", 0)

    initiative_modifier = (
        initiative_modifier_adjustments["adjustment_total"]
        + weapon_initiative_modifier
        + combatant["combat_modifiers"]["initiative_modifier"]
    )

    initiative_modifier_data = {
        "total_initiative_modifier": initiative_modifier,
        "base_initiative_modifier": combatant["combat_modifiers"]["initiative_modifier"],
        "weapon_initiative_modifier": weapon_initiative_modifier,
        "adjustment_total": initiative_modifier_adjustments["adjustment_total"],
        "adjustments": initiative_modifier_adjustments["adjustments"]
    }

    return initiative_modifier_data

def resolve_attack_roll(attack_modifier, modified_ac):
    attack_roll = {
        "hit": False
    }

    attack_roll["modified_attack_roll"] = (
        roll("d20") 
        + attack_modifier
    )

    if attack_roll["modified_attack_roll"] >= modified_ac:
        attack_roll["hit"] = True
    return attack_roll

def get_equipped_weapons(combatant, weapons):
    equipped_weapons = {}

    main_hand_id = combatant["equipped_items"]["weapons"]["main_hand"]
    off_hand_id = combatant["equipped_items"]["weapons"]["off_hand"]

    equipped_weapons["main_hand"] = weapons[main_hand_id] if main_hand_id else None
    equipped_weapons["off_hand"] = weapons[off_hand_id] if off_hand_id else None

    return equipped_weapons

def get_equipped_armor(combatant, armor):
    equipped_armor = {}

    armor_id = combatant["equipped_items"]["armor"]["body"]
    shield_id = combatant["equipped_items"]["armor"]["shield"]

    equipped_armor["body"] = armor[armor_id] if armor_id else None
    equipped_armor["shield"] = armor[shield_id] if shield_id else None

    return equipped_armor


def apply_damage(target, damage):
    hp_remaining = max(
        target["hit_points"]["hp_current"] - damage,
        0
    )
    target["hit_points"]["hp_current"] = hp_remaining
    return hp_remaining

def resolve_damage(combatant, target, damage):
    damage_roll = roll(damage) + combatant["combat_modifiers"]["damage_modifier"]
    hp_current = target["hit_points"]["hp_current"]

    apply_damage(target, damage_roll)

    damage_dealt = min(damage_roll, hp_current)

    return damage_dealt

def calculate_initiative(initiative_modifier):
    initiative_roll = roll("d6") + initiative_modifier
    return initiative_roll

def calculate_initiative_order(combatants):
    initiative_order = []
    ties_still_exist = True

    for combatant in combatants:
        combatant_order = {}
        combatant_order["combatant"] = combatant
        initiative_modifier_adjustments = calculate_adjustments(
            combatant["combat_adjustments"]["initiative_modifier"]
        )
        initiative_modifier_data = calculate_initiative_modifiers(
            combatant,
            get_equipped_weapons(combatant, weapons)["main_hand"],
            initiative_modifier_adjustments
        )
        combatant_order["initiative_modifier"] = initiative_modifier_data["total_initiative_modifier"]
        combatant_order["initiative"] = calculate_initiative(combatant_order["initiative_modifier"])
        initiative_order.append(combatant_order)
    
    while ties_still_exist:
        ties_still_exist = False
        initiative_counts = {}
        for combatant in initiative_order:
            if combatant["initiative"] in initiative_counts:
                initiative_counts[combatant["initiative"]] += 1
                ties_still_exist = True
            else:
                initiative_counts[combatant["initiative"]] = 1

        for initiative, count in initiative_counts.items():
            if count > 1:
                for combatant in initiative_order:
                    if combatant["initiative"] == initiative:
                        combatant["initiative"] = calculate_initiative(combatant["initiative_modifier"])

    initiative_order.sort(
        key=lambda initiative_record: initiative_record["initiative"], 
        reverse=True
    )
    return initiative_order

def select_target(combatant, combatants):
    valid_target = []
    if combatant["type"] == "character":
        for target in combatants:
            if target["hit_points"]["hp_current"] > 0 and target["type"] != "character":
                valid_target.append(target)
    else:
        for target in combatants:
            if target["hit_points"]["hp_current"] > 0 and target["type"] == "character":
                valid_target.append(target)
    return valid_target[0] if valid_target else None

def is_defeated(combatant):
    # TODO: Drop defeated combatant's equipped items into encounter loot.
    # is_defeated()          → determine state
    # drop_equipped_items() → move equipment into encounter loot
    # loot_items()           → later player chooses what to take
    return True if combatant["hit_points"]["hp_current"] <= 0 else False

def resolve_combat(combatants):
    initiative_order = calculate_initiative_order(combatants)
    round_number = 1
    combat_log = []
    combat_continues = True
    while combat_continues:
        for initiative_record in initiative_order:
            combatant = initiative_record["combatant"]

            if combatant["hit_points"]["hp_current"] > 0:
                target = select_target(combatant, combatants)

                if target is None:
                    combat_continues = False
                    break

                # Gathering init and combatant data for combat log. 
                attack_data = {}
                attack_data["round_number"] = round_number
                attack_data["attacker"] = combatant["name"]
                attack_data["target"] = target["name"]

                combatant_equipped_weapons = get_equipped_weapons(combatant, weapons)
                attack_modifier_adjustments = calculate_adjustments(combatant["combat_adjustments"]["hit_modifier"])
                attack_modifiers = calculate_attack_modifiers(
                    combatant,
                    combatant_equipped_weapons["main_hand"],
                    attack_modifier_adjustments
                )
                target_equipped_armor = get_equipped_armor(target, armor)
                defense_modifier_adjustments = calculate_adjustments(target["combat_adjustments"]["defense_modifier"])
                target_armor_class = calculate_modified_ac(
                    target_equipped_armor,
                    defense_modifier_adjustments
                )
                attack_roll = resolve_attack_roll(attack_modifiers["total_hit_modifier"], target_armor_class["modified_ac"])

                # Gathering attack roll/damage data for combat log.
                attack_data["attack_roll"] = attack_roll["modified_attack_roll"]
                attack_data["hit"] = attack_roll["hit"]
                attack_data["damage"] = 0

                if attack_roll["hit"]:
                    weapon = get_equipped_weapons(combatant, weapons)
                    if weapon["main_hand"]:
                        damage_dealt = resolve_damage(
                            combatant,
                            target, 
                            weapon["main_hand"]["damage"]
                        )

                        # Updating attack damage data for combat log.
                        attack_data["damage"] = damage_dealt

                record_combat_log(attack_data, combat_log)
                    # TODO: Add off-hand attack logic.
                    # If an off-hand weapon is equipped, resolve a separate attack roll
                    # before resolving off-hand damage.
                    # if weapon["off_hand"]:
                    #     resolve_damage(combatant, target, weapon["off_hand"]["damage"])

    return combat_log

def analyze_attack_enemies(character, enemies, weapon):
    attack_summary = {
        "attacks": 0,
        "hits": 0,
        "misses": 0,
        "total_damage": 0,
        "defeated": 0
    }
    for enemy in enemies:
        attack_summary["attacks"] += 1
        if resolve_attack_roll(character, enemy): #hit is scored
            attack_summary["hits"] += 1
            damage = roll(weapon["damage"]) + character["combat_modifiers"]["damage_modifier"]
            hp_current = enemy["hit_points"]["hp_current"]
            adjusted_damage = min(damage, hp_current)
            apply_damage(enemy, damage)
            attack_summary["total_damage"] += adjusted_damage
            
            if enemy["hit_points"]["hp_current"] == 0:
                attack_summary["defeated"] += 1
        else:
            attack_summary["misses"] += 1
    return attack_summary

def record_combat_log(attack, combat_log):
    combat_log.append(attack)
    return combat_log

character = character["Conan"]
target = enemies["goblin"]

def create_character(character):
    roll_character_ability_scores(character)
    # calculate_combat_modifiers(character, equipped_weapons, adjustments=None)
    calculate_hit_points(character)
    return character


# NPC functions
def create_enemy_group(enemies, enemy_name, number_of_enemies):
    enemy_group = []
    for enemy_number in range(1, number_of_enemies + 1):
        enemy_entry = deepcopy(enemies[enemy_name])
        enemy_entry["enemy_id"] = f"{enemy_name}_{enemy_number}"
        enemy_group.append(enemy_entry)
    return enemy_group


create_character(character)
enemy_group = create_enemy_group(enemies, "goblin", 3)
combatants = [character] + enemy_group

adjustments = {
    "hit_modifiers": {
        "bless": 1
    },
    "damage_modifiers": {}
}

calculate_initiative_order(combatants)
resolve_combat(combatants)

# Fighter data
## Strength scorce
## Constitution score
## Hit modifier (derived from class progression and strength)
## Damage modifier (derived from strength and specialization)
## Hit points (max at first level and constitution bonus)
# Strength
#    ├── contributes to hit modifier
#    └── contributes to damage modifier

# Constitution
#    └── contributes to hit points

# Class + level
#    └── contributes to hit modifier


# Goblin data

# Dice rolling

# Attack resolution

# Combat loop

# Goals
# Create Fighter
#      ↓
# Create Goblin
#      ↓
# Roll initiative
#      ↓
# Fighter attacks
#      ↓
# Goblin attacks
#      ↓
# Repeat
#      ↓
# Someone reaches 0 HP
#      ↓
# Combat ends
#