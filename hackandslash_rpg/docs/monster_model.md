# Monster Model

The monster model currently contains both game-owned monster properties and values used by individual combatants at runtime. As the model evolves, canonical monster definitions will be separated from mutable runtime monster state.

## Current Structure

The following represents the current monster structure used by the game. Some fields are still being refined as OSE normalization progresses, and the separation between canonical definitions and runtime state is not yet complete. The string `attacks` and `damage` fields below remain in `main.py`; the importer now produces the separate structured attack representation described below. Runtime migration is pending.

```python
"goblin": {
    "name": "goblin",
    "type": "monstrous humanoid",

    "armor_class": {
        "base_ac": 13,
        "shield_bonus": 0
    },

    "hit_dice": {
        "number_of_dice": 1,
        "die": "d8",
        "hp_modifier": 0,
        "special": False
    },

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
}
```

## Model Principles

- Monster definitions represent static game data.
- Runtime monsters are created from monster definitions.
- Runtime state must not modify the underlying definition.
- Values that can be derived reliably should generally be calculated rather than duplicated.
- The monster model should represent game concepts rather than OSE source formatting.
- Unusual monster mechanics should not unnecessarily complicate the common monster schema.

## Current Normalization Status

The monster schema is still evolving as OSE fields are normalized.

| Field | Status |
|---|---|
| Armor Class | Normalized |
| Hit Dice | Normalized |
| Attacks | First pass implemented; correctness fixes and runtime integration pending |
| Attack Modifier / THAC0 | Pending |
| Movement | Pending |
| Saving Throws | Pending |
| Morale | Pending |
| Alignment | Pending |
| Experience | Pending |
| Number Appearing | Pending |
| Treasure Type | Pending |

Fields that have not yet been normalized should be considered **provisional**, even if they already exist in the current monster object.

## Normalized Attack Representation

The importer returns a list of attack options. Choose one option; the attacks keyed by name within it form a combined routine. For example, Hellhound's bite and breath are alternatives:

```python
"attacks": [
    {
        "bite": {
            "attack_name": "bite",
            "number_of_attacks": 1,
            "damage_dice": "1d6",
            "damage_modifier": 0,
            "effects": [],
        },
    },
    {
        "breath": {
            "attack_name": "breath",
            "number_of_attacks": 1,
            "damage_dice": "1d6 per Hit Die",
            "damage_modifier": 0,
            "effects": [],
        },
    },
]
```

Griffon's claws and bite instead occupy the same option dictionary. Names are lowercased, omitted counts default to `1`, and bare attack names or effect-only attacks have `damage_dice = None`. Effects remain text; `damage_dice` also preserves scaling and multiplied expressions awaiting runtime interpretation.

The common parser supports counted attacks, outside-parentheses combinations and alternatives, enclosing routine brackets, two-name shared damage, and selection of weapon-dependent damage in recognized `/` alternatives. The source literal `None` currently becomes an entry keyed by Python `None`, with count `0`; it is not represented as an empty list.

Ranged attack counts have `number_of_attacks = None` and `requires_enrichment = True`. The current `source_attack_string` contains only the count text; retain the complete imported OSE record for enrichment. Unresolved counts must not be treated as executable attack routines.

Normalization does not resolve spells, poison, additional heat damage, HD scaling, damage multiplication, or equipment-dependent damage. Nested choices such as Chimera require source review and dedicated handling; they are not automatically detected as deferred.

Integer bonuses and penalties are stored separately in `damage_modifier`. Additional damage such as `1d10 heat` remains in `effects`.

Duplicate attack names can still overwrite entries. See the normalization decisions for remaining parsing limitations and deferred behavior.

See [normalization decisions](decisions/normalization.md#attacks) for the detailed supported patterns and implementation discrepancies. This representation has not replaced the legacy runtime fields shown above.

## Special Cases

Some monsters have mechanics that do not fit the common model.

These should first be handled using the simplest usable representation while preserving the original imported source data.

For example, OSE monsters with Hit Dice ranges currently normalize to the lowest HD value and set:

```python
"special": True
```

More complete variants can be introduced during enrichment.

Monsters with fundamentally unusual mechanics, such as the Hydra, may eventually require dedicated special-rule behavior rather than expanding the common schema for every monster.
