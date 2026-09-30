# Character Object

The character object stores the character's **persistent state**. Values that can be calculated from that state should generally be derived rather than stored separately.

## Structure

```text
CHARACTER — Persistent State
│
├── name / identity
├── class
│   ├── name
│   └── level
├── ability_scores
├── hit_points
├── combat_modifiers
├── combat_adjustments
├── equipped_items
└── inventory

              ↓ calculations ↓

DERIVED / CONTEXTUAL VALUES
│
├── effective attack modifier
├── effective damage modifier
├── effective AC
├── initiative
├── encumbrance
└── saves, movement, etc.

              ↓

OUTPUT
├── combat resolution
├── combat log
└── character sheet
```

## Design Principle

**Store state; calculate derived values.**

For example, the character stores Strength, equipped weapons, and temporary combat adjustments. The effective attack and damage modifiers are calculated from those values when needed.

This keeps the character object as the source of truth while avoiding duplicated values that could become inconsistent.
