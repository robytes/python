# OSE Monster Import Pipeline

This document describes the pipeline used to import monster data from the Old-School Essentials (OSE) rules reference into the game's internal monster model.

The main design principle is:

> **Preserve external source data first. Validate it. Then convert it into the game's internal representation.**

This keeps source-specific parsing separate from game logic and provides a reusable pattern for future external datasets and API integrations.

---

## Pipeline Overview

```text
OSE Website
    ↓
1. Retrieve
    ↓
2. Extract
    ↓
3. Parse
    ↓
4. Validate
    ↓
5. Normalize
    ↓
6. Enrich
    ↓
7. Output
    ↓
Canonical Monster Definitions
```

---

## 1. Retrieve

Retrieve data from the external source without interpreting it.

Examples:

```text
OSE monster list page
    ↓
Monster links
    ↓
Individual monster pages
```

Responsibilities include:

* Sending HTTP requests.
* Checking HTTP response status.
* Retrieving source HTML.
* Discovering monster links.
* Retrieving individual monster pages.

At this stage, the importer should know as little as possible about the game's monster model.

---

## 2. Extract

Extract relevant content from the external document structure.

For OSE monsters this includes:

* Monster name
* Description
* Raw statistics
* Source grouping information

Example:

```text
Zombie

Listless humanoid corpses...

AC 8 [11] HD 2 (9hp) Att Weapon...
```

becomes approximately:

```python
{
    "name": "Zombie",
    "source_group": None,
    "description": "Listless humanoid corpses...",
    "stats": {
        "raw": "AC 8 [11] HD 2 (9hp) Att Weapon...",
        "formatted": {}
    }
}
```

### Grouped OSE Pages

Some OSE pages contain multiple individually statted monsters.

Example:

```text
Hawk
├── Giant Hawk
└── Normal Hawk
```

or:

```text
Lycanthrope
├── Devil Swine
├── Werebear
├── Wereboar
├── Wererat
├── Weretiger
└── Werewolf
```

OSE identifies these entries with `<h4>` subheadings.

The importer flattens them into individual records:

```text
Hawk page
    ↓
Giant Hawk → source_group = "Hawk"
Normal Hawk → source_group = "Hawk"
```

The source grouping is preserved as metadata. It does **not** automatically become the game's monster type.

---

## 3. Parse

Convert the raw source text into identifiable OSE fields without yet changing their meaning.

Example raw data:

```text
AC 5 [14] HD 4* (18hp) Att Bite (2d4) THAC0 16 [+3] ...
```

becomes:

```python
{
    "AC": "5 [14]",
    "HD": "4* (18hp)",
    "Att": "Bite (2d4)",
    "THAC0": "16 [+3]",
    "MV": "180′ (60′)",
    "SV": "D10 W11 P12 B13 S14 (4)",
    "ML": "8",
    "AL": "Chaotic",
    "XP": "125",
    "NA": "1d6 (2d6)",
    "TT": "C"
}
```

The parser should answer:

> **What does OSE say?**

It should not yet answer:

> **What does this mean in our game?**

Keeping these responsibilities separate prevents OSE's representation from becoming the game's internal data model.

---

## 4. Validate

Validate that the imported source data matches the assumptions made by the parser.

For example, the OSE parser expects the following stat markers:

```python
OSE_STAT_MARKERS = [
    "AC",
    "HD",
    "Att",
    "THAC0",
    "MV",
    "SV",
    "ML",
    "AL",
    "XP",
    "NA",
    "TT"
]
```

Validation checks that expected markers actually exist in the raw source data.

This is important because:

```python
raw_stats.find(marker)
```

returns:

```python
-1
```

when a marker is missing.

Python slicing may still succeed with a `-1` index, potentially producing incorrect data without raising an exception.

Validation therefore answers:

> **Did the import produce the OSE data we expected?**

Validation should remain separate from parsing.

A useful general integration pattern is:

```text
Retrieve
    ↓
Extract
    ↓
Parse
    ↓
Validate
```

This pattern can be reused for other imported game datasets.

---

## 5. Normalize

Normalization converts source-specific values into the game's canonical representation.

Example:

```text
OSE:

AC = "5 [14]"
```

might normalize to:

```python
{
    "armor_class": 14
}
```

Likewise:

```text
OSE:

HD = "4* (18hp)"
```

may eventually become structured game data such as:

```python
{
    "hit_dice": 4,
    "average_hp": 18,
    "special_ability_markers": 1
}
```

Normalization answers:

> **What does this source data mean to our game?**

Normalization is part of the overall import pipeline, but should remain separate from source parsing.

```text
parse_ose_monster_stats()
        ↓
"What does OSE say?"

normalize_monster()
        ↓
"What does that mean to our game?"
```

---

## 6. Enrich

Once source data has been normalized into the game's schema, additional sources may provide information missing from OSE.

Potential enrichment sources may provide:

* Missing descriptions
* Monster types
* Monster subtypes
* Special abilities
* Immunities
* Resistances
* Movement types
* Senses
* Languages
* Other useful classifications

The intended architecture is:

```text
OSE ──────────┐
              │
              ↓
        Canonical Schema
              ↑
              │
d20 / 3.x ────┘
```

External sources should contribute information to the game's schema rather than dictate that schema.

Source provenance should be retained when practical so imported or enriched information can be traced back to its origin.

---

## 7. Output

The final result should be a canonical monster definition owned by the game rather than by OSE, d20, or another external system.

Conceptually:

```text
External Sources
      ↓
Import / Enrichment
      ↓
Canonical Monster Definition
      ↓
JSON / Data Store
      ↓
Runtime Monster Instance
```

Eventually individual monster definitions may be stored as:

```text
monsters/
└── definitions/
    ├── goblin.json
    ├── zombie.json
    ├── werewolf.json
    └── giant_hawk.json
```

These definitions represent static game content.

Runtime monsters should be created from those definitions rather than modifying the definitions themselves.

---

# Source Data vs Game Data

A critical architectural boundary is:

```text
SOURCE DATA
"What did the external system give us?"

            ↓

NORMALIZATION / ENRICHMENT

            ↓

GAME DATA
"What does our application need?"
```

For example:

```text
OSE webpage organization:
Lycanthrope
├── Werebear
└── Werewolf
```

does not necessarily imply:

```text
monster_type = "lycanthrope"
```

Instead, the importer can faithfully preserve:

```python
{
    "name": "Werewolf",
    "source_group": "Lycanthrope"
}
```

A later normalization or classification stage determines whether `lycanthrope` should become a type, subtype, tag, template, or another game concept.
## OSE Monster Normalization Map

This table defines how each parsed OSE monster statistic is handled when
converting imported OSE data into the game's internal monster schema.

| OSE Stat | Action | Game Schema Target | Normalization Rule |
|---|---|---|---|
| `AC` | Normalize | `armor_class` | Extract ascending AC. Determine armor/equipment separately where appropriate. |
| `HD` | Normalize | `hit_dice` | Parse hit-dice count and modifiers. HP is rolled during instantiation. |
| `Att` | Normalize | `attacks` | Parse attack count, attack type, and damage information. |
| `THAC0` | Normalize | `combat_modifiers.hit_modifier` | Discard THAC0 value and retain ascending attack modifier. |
| `MV` | Normalize | `movement` | Convert movement values into structured numeric feet values. |
| `SV` | Normalize | `saving_throws` | Parse Death, Wands, Paralysis, Breath, Spells, and save-as level. |
| `ML` | Direct | `morale` | Convert value to integer. |
| `AL` | Direct | `alignment` | Normalize formatting/case. |
| `XP` | Direct | `experience.xp_value` | Convert value to integer. |
| `NA` | Normalize | `number_appearing` | Separate dungeon and wilderness encounter expressions. |
| `TT` | Direct / Reference | `inventory.treasure` | Preserve treasure type. Treasure is generated during instantiation. |

### Normalization Boundaries

Normalization only translates information supplied by OSE into the game's
schema.

For example:

    OSE:
    AC 6 [13]

            ↓ Normalize

    Game definition:
    armor_class.base_ac = 13

Determining that an AC 13 humanoid is specifically wearing chain mail may
require additional game rules or external information and is therefore not
necessarily part of basic OSE normalization.

Likewise:

    OSE:
    HD 1 (4 hp)

            ↓ Normalize

    Game definition:
    hit_dice.number = 1
    hit_dice.die = "d8"
    hit_dice.modifier = 0

            ↓ Instantiate

    Individual Orc:
    hp_max = roll("1d8")
    hp_current = hp_max

The normalization layer should not generate runtime state such as rolled hit
points, randomly selected equipment, or generated treasure.

### Monster Type and Equipment Derivation

First-pass normalization should translate OSE statistics into structured game
data without attempting to explain how those statistics were produced.

For example:

    OSE:
    AC 6 [13]

        ↓ Normalize

    armor_class.base_ac = 13

A later derivation stage may use `monster_type` and other game rules to determine
the source of that AC.

For equipment-capable creatures such as monstrous humanoids, an AC value may be
represented by worn armor. For example, an Orc or Goblin with AC 13 could be
assigned armor capable of producing AC 13.

For creatures that do not normally use equipment, such as animals, the same AC
value should generally represent natural or inherent defenses rather than worn
armor.

Conceptually:

    AC 13
      ↓
    Monster Type
      ↓
    ├── Monstrous Humanoid → equipment-capable → derive appropriate armor
    └── Animal             → no armor          → treat AC as natural/inherent

Monster type should therefore eventually describe capabilities such as whether
a creature can use armor or weapons. This avoids hard-coding rules for individual
monster names.

This logic belongs to derivation rather than first-pass OSE normalization.

---

# High-Level Import Function

Eventually the individual pipeline stages may be orchestrated by a high-level function:

```python
import_ose_monsters()
```

Conceptually:

```text
import_ose_monsters()

    get source page
          ↓
    discover monster links
          ↓
    retrieve monster pages
          ↓
    extract monster records
          ↓
    flatten grouped records
          ↓
    parse OSE statistics
          ↓
    validate imported data
          ↓
    normalize to game schema
          ↓
    enrich where appropriate
          ↓
    output canonical records
```

Each stage should remain independently understandable and testable even if a single function eventually coordinates the entire workflow.

---

# Reusable Integration Pattern

The larger lesson from the OSE importer is applicable beyond monster scraping.

For any external dataset or API:

```text
EXTERNAL SYSTEM
      ↓
Retrieve
      ↓
Extract / Deserialize
      ↓
Parse
      ↓
Validate
      ↓
Normalize
      ↓
Enrich
      ↓
INTERNAL DOMAIN MODEL
```

The external representation should stop at the integration boundary.

The rest of the application should operate on data structures defined by the application itself.
