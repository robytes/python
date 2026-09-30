# Hack-and-Slash RPG

A Python-based old-school fantasy RPG engine inspired primarily by **D&D Rules Cyclopedia (RC)** and **Old-School Essentials (OSE)**.

The current focus is building reusable combat mechanics and a data pipeline for converting OSE monster data into game-owned monster definitions.

The long-term goal is to support a text-based multiplayer RPG while keeping the core rules engine independent from any specific UI, networking, or persistence framework.

## Design Goals

* Use **Rules Cyclopedia / BECMI** as the primary rules foundation.
* Use **OSE** as a compatible source for monster and rules data.
* Use **ascending Armor Class** following the OSE model (`19 - descending AC`).
* Borrow useful concepts from later D&D editions and other games without replacing the RC foundation.
* Keep external source formats separate from the internal game model.
* Keep static definitions separate from mutable runtime instances.
* Store state and calculate derived values where practical.
* Build abstractions in response to actual game requirements.

## Current Systems

### Characters

Characters currently support:

* Ability scores and modifiers
* Class and level
* Hit points
* Combat modifiers
* Temporary combat adjustments
* Equipped weapons and armor
* Inventory

### Combat

Moving characters and enemies toward a common combat-facing interface.

```text id="a7d3hr"
combat_modifiers
├── hit_modifier
├── damage_modifier
└── initiative_modifier

combat_adjustments
├── hit_modifier
├── damage_modifier
├── defense_modifier
└── initiative_modifier
```

Combat calculations combine established capability, equipment, and temporary adjustments to produce final values consumed by attack, damage, AC, and initiative resolution.

Initiative is rolled once at the beginning of combat, ties are rerolled, and the resulting order remains fixed for the encounter.

### Enemies

The existing enemy model supports:

* Armor Class
* Hit dice and hit points
* Combat modifiers and adjustments
* Attacks and damage
* Equipped items
* Inventory

The model is being expanded to support additional RC/OSE monster information such as movement, saving throws, morale, alignment, XP, number appearing, and treasure.

## OSE Monster Importer

The current major development effort is an importer for the OSE monster reference.

It currently:

* Retrieves the OSE monster index and individual monster pages.
* Parses HTML using BeautifulSoup.
* Extracts monster descriptions and statistics.
* Handles pages containing multiple related monsters.
* Flattens grouped monsters into individual records.
* Parses the standard OSE monster statistics.
* Handles monsters with missing descriptions.
* Validates imported stat blocks before normalization.

The importer currently recognizes:

```text id="eaj41c"
AC   HD   Att   THAC0   MV   SV
ML   AL   XP    NA      TT
```

## Data Pipeline

```text id="o6x8zu"
OSE Source
    ↓
Import
    ↓
Validate
    ↓
Normalize        ← CURRENT
    ↓
Derive
    ↓
Enrich
    ↓
Canonical Monster Definition
    ↓
Instantiate
    ↓
Runtime Enemy
```

### Normalize

Normalization converts OSE representations into the game's structured representation.

For example:

```text id="77wcbp"
OSE
AC 6 [13]

    ↓

Game
armor_class.base_ac = 13
```

The first pass is intentionally mechanical. It does not yet determine why a monster has a particular AC or assign randomly generated equipment.

Each OSE statistic will eventually have a focused normalizer:

```python id="0c6alw"
normalize_armor_class()
normalize_hit_dice()
normalize_attacks()
normalize_attack_modifier()
normalize_movement()
normalize_saving_throws()
normalize_morale()
normalize_alignment()
normalize_experience()
normalize_number_appearing()
normalize_treasure_type()
```

### Derive

Derivation applies game rules to normalized data.

For example, monster type will eventually determine whether an AC represents worn armor or natural defenses:

```text id="u22e4u"
AC 13
  ↓
Monster Type
  ├── Monstrous Humanoid → potentially worn armor
  └── Animal             → natural/inherent AC
```

Deliberately keeping this logic outside first-pass normalization.

### Enrich

Enrichment adds information OSE does not provide.

Potential enrichment includes:

* Ability scores
* Monster types and subtypes
* Additional traits and abilities
* Immunities and resistances
* Senses and languages
* Missing descriptions

Additional rules sources may be used for enrichment while the game's own schema remains authoritative.

### Instantiate

Definitions describe what a monster **is**. Instantiation creates an individual runtime enemy.

For example:

```text id="8q8fln"
Orc Definition
HD = 1d8
    ↓
Instantiate
    ↓
Orc #1
HP = roll("1d8")
```

Instantiation will eventually handle rolled HP, equipment selection, treasure generation, and encounter-specific state.

## Current State

Implemented or substantially working:

* Dice rolling with modifiers
* Character data model
* Equipment and inventory structure
* Combat modifiers and temporary adjustments
* Attack and AC calculations
* Individual initiative and initiative ordering
* Basic enemy definitions
* OSE HTTP retrieval
* Monster-link discovery
* Monster-page extraction
* Grouped monster handling
* OSE stat parsing
* Missing-description handling
* Import validation

**Current development phase:** OSE monster normalization.

## Next Steps

1. **Normalize Armor Class**

   * Start with standard values such as `"6 [13]" → base_ac = 13`.
   * Inspect the complete dataset for alternate AC formats.

2. **Normalize remaining OSE statistics**

   * HD, attacks, attack modifier, movement, saves, morale, alignment, XP, number appearing, and treasure type.

3. **Build a prototype canonical monster**

   * Use a straightforward monster such as an Orc.
   * Keep the result in memory until the schema stabilizes.

4. **Test different monster shapes**

   * Orc — humanoid / weapon user
   * Wolf — animal / natural attack
   * Zombie — undead
   * Chimera — multiple attacks and movement
   * Werewolf — alternate forms / AC

5. **Stabilize the monster schema**

   * Once representative monsters normalize successfully, begin storing canonical definitions as JSON.

6. **Document architecture**

   * Consolidate established design decisions and create durable project context before beginning enrichment.

7. **Begin enrichment and instantiation**

   * Add information unavailable from OSE, then build runtime enemies from the resulting definitions.

8. **Continue combat development**

   * Complete damage handling, reconnect the attack sequence, and progress toward full encounter resolution.

## Longer-Term Direction

Canonical monster definitions will eventually be stored separately from runtime state:

```text id="2x18nn"
Monster Definitions
       ↓
Rules Engine
       ↓
Runtime Instances
       ↓
Persistence
       ↓
Multiplayer Application
```

A framework such as Evennia may eventually provide persistence, commands, sessions, and multiplayer infrastructure, while the core RPG rules engine remains independently testable.
