# OSE Monster Normalization Decisions

This document records decisions made while normalizing OSE monster data into the game's internal monster model.

It is intended to prevent settled normalization decisions from being repeatedly reconsidered as development continues.

For the overall import process, see `docs/pipelines/ose_monster_import.md`.

## General Principles

- Normalize information actually supplied by OSE.
- Do not infer additional mechanics during normalization unless required by the game's canonical representation.
- Preserve imported source data when information is intentionally deferred.
- Runtime values such as rolled hit points are created during instantiation, not normalization.
- Exceptional monsters should not unnecessarily complicate the common monster schema.

## Armor Class

**Status:** Complete

OSE ascending Armor Class is used as the canonical base AC.

Example:

```text
OSE:
AC 6 [13]

Normalized:
armor_class.base_ac = 13
```

When OSE supplies multiple AC values, the additional value may be preserved as a secondary AC without attempting to determine its meaning during normalization.

Any monster with a secondary AC must be reviewed during enrichment. Use the preserved OSE source text to determine when the secondary AC applies and what game state or rules are needed to support it. For example, `3 [16] (9 [10] in human form)` requires evaluation of the human-form condition before the secondary AC can be used by the rules engine. Automatic condition extraction and its canonical representation remain deferred.

Armor, shields, natural defenses, and other explanations for the resulting AC are not derived during basic normalization.

## Hit Dice

**Status:** Complete

Monster Hit Dice use `d8`, following the RC/BECMI standard.

Normalized structure:

```python
"hit_dice": {
    "number_of_dice": 1,
    "die": "d8",
    "hp_modifier": 0,
    "special": False
}
```

### Modifiers

OSE HD modifiers are preserved.

```text
4+1 → 4d8 + 1
5-1 → 5d8 - 1
```

### Fractional Hit Dice

OSE `½` HD is represented as:

```python
"number_of_dice": 0.5
```

### Asterisks

OSE Hit Dice asterisks are not retained as part of the normalized HD value.

They indicate special abilities affecting XP calculation, while XP is imported separately.

### Parenthetical Hit Points

Parenthetical HP values supplied by OSE are not promoted into the canonical Hit Dice structure.

For example:

```text
4+1 (19hp)
```

normalizes the `4+1` HD expression. Runtime HP is generated from the normalized Hit Dice when a monster is instantiated.

### Hit Dice Ranges

OSE monsters expressed using an HD range currently normalize to the **lowest value in the range**.

Example:

```text
3 to 7*
```

currently uses:

```python
"number_of_dice": 3
"special": True
```

The original imported OSE value remains available for later processing.

Complete versions of these monsters are deferred to enrichment, where HD changes can be coordinated with other properties such as attack modifiers, saving throws, and XP.

### Exceptional Monsters

Some monsters may require dedicated special-rule behavior rather than additional complexity in the common monster schema.

The Hydra is the primary current example: its HD range and HP behavior are sufficiently unusual that the generic HD model should not be redesigned solely to accommodate it.

## Attacks

**Status:** Implemented first pass; correctness limitations and enrichment work remain.

`normalize_attacks()` in `importers/ose_importer.py` returns a list of alternative attack routines. Each routine is a dictionary keyed by attack name. Attacks within one dictionary are used together; separate dictionaries represent alternatives. This is importer output, not yet integration with the runtime combat engine.

### Structure

For `2 × claw (1d4) + bite (2d8)`:

```python
"attacks": [
    {
        "claw": {
            "attack_name": "claw",
            "number_of_attacks": 2,
            "damage_dice": "1d4",
            "damage_modifier": 0,
            "effects": [],
        },
        "bite": {
            "attack_name": "bite",
            "number_of_attacks": 1,
            "damage_dice": "2d8",
            "damage_modifier": 0,
            "effects": [],
        },
    },
]
```

Names are stripped and lowercased. Ordinary attack counts default to `1`, damage defaults to `None`, modifiers default to `0`, and effects default to an empty list. `damage_dice` can contain preserved expressions, not only directly rollable dice strings.

### Supported Patterns

- Single and counted attacks, such as `Butt (1d8)` and `2 × claw (1d4)`.
- Combined attacks separated by `+` outside parentheses.
- Alternatives separated by the literal ` or ` outside parentheses. Operators within parentheses remain part of the attack details.
- One enclosing square-bracket pair around a routine, such as `[gore (1d6) + bite (1d6)] or weapon (1d6)`.
- Shared parenthesized details for two alternatives when the first has no opening parenthesis, such as `Talons or beak (1d6)`.
- Damage with textual effects, such as `Sting (1d3 + poison + lodged stinger)`, and effect-only attacks such as `Song (charm)`.
- Bare names such as `spell` and `lightning bolt`, retained with unspecified damage. Bare counted names are not separately parsed.
- The literal `None`, returned as an attack with name `None`, count `0`, and otherwise default values. The outer result is a one-option list with a Python `None` dictionary key, rather than an empty attack list.
- Weapon damage alternatives: a recognized `weapon damage die` expression on the right side of `/`, optionally with a modifier, replaces the fixed-damage alternative. Fixed weapon damage without that alternative remains unchanged.
- Integer bonuses and penalties are stored in `damage_modifier`, not `effects`. Observed `+ 2` and `– 1` formats are supported.
- Additional damage such as `1d10 heat` remains text in `effects` for later interpretation.

### Deferred Behavior and Current Limitations

Attack-count ranges, such as Hydra's `5 to 12`, use `number_of_attacks = None` and add `requires_enrichment = True`. The current `source_attack_string` field stores only the count expression, despite its name. Full attack information remains in the imported `stats.formatted.Att` and raw source; do not discard those records. Enrichment must resolve these counts before runtime use.

Expressions such as `1d6 per Hit Die`, `1d6 × 10`, and additional damage effects such as `1d10 heat` remain text. Spell identification, effect mechanics, scaling, multiplication, equipment damage resolution, and the relationship between imported bonuses and future ability scores are not implemented by normalization.

Chimera-style nested square-bracket choices remain unsupported. The splitter tracks parentheses only; it neither understands nested choices nor explicitly marks them as deferred. Such records require review against the preserved source before canonical use.

The following are implementation discrepancies requiring correction, not intended game rules:

- Damage classification uses the presence of any digit in the first part, not validation of a dice expression.
- Shared-detail copying does not validate the second closing parenthesis before slicing. General single-attack parsing rejects missing or reversed parentheses, but is not full syntax validation.
- Repeated attack names within a routine overwrite earlier entries because names are dictionary keys.

Completing a pass over the source monsters does not establish correctness for these cases. The legacy `attacks` and `damage` fields in `main.py` have not been migrated to this representation.

## Remaining Fields

The following fields have not yet been normalized and their final representations remain provisional:

- THAC0 / attack modifier
- Movement
- Saving throws
- Morale
- Alignment
- Experience
- Number appearing
- Treasure type

Decisions for these fields should be added to this document as they are made.
