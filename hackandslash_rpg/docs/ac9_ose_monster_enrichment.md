# AC9 and OSE Monster Enrichment

## Purpose

After OSE normalization is complete, compare the OSE monster catalog against the BECMI **AC9 Creature Catalogue**.

Goals:

* Identify AC9 monsters missing from OSE.
* Identify useful AC9 data for monsters that exist in both sources.
* Use BECMI-native information where possible before looking to later editions for enrichment.

## Comparison

```text id="snzhd9"
OSE Monsters        AC9 Monsters
     │                    │
     └─────────┬──────────┘
               ↓
            Compare
               ↓
     ┌─────────┼─────────┐
     ↓         ↓         ↓
   Both     OSE Only   AC9 Only
     ↓                   ↓
  Enrich             Add Later
```

For monsters present in both sources, examine AC9 for useful information not provided by OSE, including:

* Creature classification
* Intelligence
* Habitat
* Description
* Special abilities
* Behavior or tactics

Do not automatically import every AC9 field. Only add information useful to the game's monster model.

## Monster Classification

AC9 groups creatures into:

```text id="vttzwj"
Animals
Conjurations
Humanoids
Lowlife
Monsters
Undead
```

Evaluate these categories as a possible BECMI-native foundation for `monster_type`.

Monster type may later help derive game behavior:

```text id="92jdq8"
Monster Type
    ↓
Capabilities
    ├── uses armor
    ├── uses weapons
    └── natural defenses
```

This belongs to **derivation**, not OSE normalization.

## Development Order

```text id="gucxst"
OSE Import / Validation
        ↓
OSE Normalization          ← Current
        ↓
Stabilize Monster Schema
        ↓
Document / Agent Checkpoint
        ↓
AC9 ↔ OSE Comparison
        ↓
Enrichment
        ↓
Canonical Monster Definitions
```

AC9-only monsters can be added after the comparison using the canonical monster schema.

## Principle

OSE provides the initial normalized monster data. AC9 supplements it with additional BECMI information.

Other sources, such as d20/3.x material, can later fill gaps that neither source provides.

The final game-owned monster definitions—not OSE, AC9, or another external source—become the runtime source of truth.
