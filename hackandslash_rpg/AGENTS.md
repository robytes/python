# Hack-and-Slash RPG Agent Instructions

## Project

This repository contains a Python hack-and-slash RPG engine based primarily on **D&D Rules Cyclopedia (RC) / BECMI**.

**Old-School Essentials (OSE)** is used as a compatible source for importing game data. OSE source structures should not become dependencies of the core game model.

The project is both:

1. A working RPG engine.
2. A project for developing and demonstrating Python and software-engineering skills.

## Source of Truth

When determining current project behavior or design, use this order of authority:

1. **Current source code**
2. **Explicit decisions in `docs/`**
3. **This file**
4. **Conversation context or assumptions**

If code and documentation disagree, identify the discrepancy rather than silently choosing a new design.

Do not treat exploratory ideas, TODOs, or provisional structures as established architecture.

## Documentation

Consult the relevant documentation before proposing architectural changes.

Key documents include:

- `docs/architecture.md` — system boundaries and architectural direction
- `docs/development_guidelines.md` — development and coaching approach
- `docs/character_object.md` — character data model
- `docs/monster_model.md` — current monster model
- `docs/core_rules.md` — core game mechanics
- `docs/house_rules.md` — intentional departures from RC/BECMI
- `docs/pipelines/ose_monster_import.md` — OSE import pipeline
- `docs/decisions/normalization.md` — settled OSE normalization decisions

When a design decision changes, update the relevant documentation rather than relying on conversation history.

## Architecture

Maintain the separation between:

```text
External Source Data
        ↓
Import / Parse
        ↓
Validate
        ↓
Normalize
        ↓
Derive / Enrich
        ↓
Canonical Definitions
        ↓
Instantiate
        ↓
Runtime State
        ↓
Rules Engine
```

External formats should stop at the integration boundary. Core game logic should operate on structures owned by the game.

Keep the rules engine independent of future persistence, networking, or multiplayer frameworks where practical.

## Development Approach

- Prefer straightforward, readable Python over clever implementations.
- Avoid premature abstraction.
- Let demonstrated game requirements drive architecture.
- Preserve existing behavior unless a change is intentional.
- Keep functions focused on clear responsibilities.
- Prefer explicit data flow and understandable data structures.
- Do not redesign established systems solely to accommodate rare edge cases.
- Preserve source information when an edge case is intentionally deferred.

Exceptional monsters such as the Hydra may require special-rule behavior rather than additional complexity in the common monster model.

## Interactive Development

This project is also used for Python practice.

For learning-oriented programming work:

- Do not immediately provide a complete implementation.
- Let the developer attempt the solution first.
- Use progressively stronger hints when needed.
- Explain relevant Python behavior and data flow.
- Break difficult problems into small steps.
- Review submitted code for correctness, readability, and complexity.
- When useful, ask the developer to explain the intended algorithm before coding.

For repetitive or non-learning work—such as documentation cleanup, mechanical transformations, or data inspection—direct solutions are appropriate.

## Current Development State

OSE monster import and validation are implemented.

Monster normalization is currently in progress.

Consult `docs/decisions/normalization.md` and `docs/monster_model.md` for the current normalization status rather than relying on this file for field-level progress.

## Guiding Principle

Build the simplest model that correctly supports the game requirements currently understood.

Do not make every monster a Hydra.