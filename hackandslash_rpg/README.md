# Hack-and-Slash RPG

A Python-based old-school fantasy RPG engine built primarily around **D&D Rules Cyclopedia (RC)** and **Old-School Essentials (OSE)**.

The project currently focuses on combat mechanics and converting external OSE monster data into structured, game-owned monster definitions. The long-term goal is a persistent, text-based multiplayer RPG.

## Design Goals

* Use **Rules Cyclopedia / BECMI** as the primary rules foundation.
* Use **OSE** as a compatible source for monster and rules data.
* Keep imported source data separate from the internal game model.
* Separate static definitions from mutable runtime state.
* Store state and calculate derived values where practical.
* Add abstractions as game requirements emerge rather than designing them prematurely.

## Core Systems

### Characters

The character model supports ability scores, class and level, hit points, combat modifiers, temporary adjustments, equipment, and inventory.

Character state feeds calculations for attack, damage, Armor Class, initiative, and other derived values.

### Combat

The combat system currently supports:

* Ascending Armor Class
* Attack and AC calculations
* Weapon damage and modifiers
* Individual initiative
* Equipment-based combat modifiers
* Temporary combat adjustments
* Character and enemy combatants

Initiative is rolled once per combat. Ties are rerolled, and the resulting order remains fixed for the encounter.

### Monsters

Monster definitions support Armor Class, Hit Dice, hit points, attacks, combat modifiers, equipment, and inventory.

The model is being expanded to represent additional RC/OSE monster data, including movement, saving throws, morale, alignment, XP, number appearing, and treasure.

## OSE Monster Importer

The project includes an importer that retrieves and parses the OSE monster reference using **Requests** and **BeautifulSoup**.

It currently handles:

* Monster index and page discovery
* HTML extraction and parsing
* Grouped monster pages
* Monster descriptions and stat blocks
* Standard OSE statistics
* Missing descriptions
* Import validation

Imported monster data is being normalized into the game's internal monster model. Detailed importer architecture, normalization, derivation, and enrichment plans are documented in the `docs/` directory.

## Current Development

Implemented or substantially working:

* Character data model
* Dice and modifier system
* Equipment and inventory
* Attack and Armor Class calculations
* Individual initiative and ordering
* Enemy definitions
* OSE web import and parsing
* Grouped monster extraction
* Stat-block parsing and validation

**Current focus:** Normalizing imported OSE monster data into the canonical monster model.

Next milestones include completing monster normalization, stabilizing the canonical schema, enriching monsters with additional BECMI data, and completing encounter resolution.

## Architecture

The project separates source data, game definitions, and runtime state:

```text
External Rules Data
        ↓
Import / Normalize
        ↓
Canonical Definitions
        ↓
Rules Engine
        ↓
Runtime Instances
        ↓
Persistence / Multiplayer
```

This keeps the rules engine independently testable and allows persistence or multiplayer frameworks to be added without defining the core game model.

## Longer-Term Direction

The goal is to evolve the project into a persistent multiplayer RPG while continuing to expand the RC/BECMI rules implementation.

Future development includes:

* Additional character classes
* Expanded combat and encounter resolution
* BECMI monster catalog enrichment
* Persistent character and world state
* Text-based multiplayer gameplay
* Potential integration with a framework such as Evennia

Detailed design decisions, house rules, data models, and import/enrichment plans are maintained in the `docs/` directory.
