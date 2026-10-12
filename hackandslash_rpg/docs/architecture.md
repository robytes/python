# Architecture

## Overview

Hack-and-Slash RPG is a Python RPG engine based primarily on **D&D Rules Cyclopedia (RC) / BECMI**, with **Old-School Essentials (OSE)** used as a compatible source of monster and rules data.

The architecture separates external source data, game-owned definitions, runtime state, and game rules.

## Data Flow

```text id="rdq6t2"
External Rules Data
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

### Import / Parse

Retrieve external data and convert source-specific formats into structures Python can process. Preserve the original imported data when practical.

### Validate

Confirm that imported records contain the expected source fields before normalization.

### Normalize

Translate source values into the game's internal representation.

Normalization should structure information already present in the source without unnecessarily deriving new game mechanics.

### Derive / Enrich

**Derivation** applies game rules or project conventions to normalized information.

**Enrichment** adds information not provided by the original source, potentially using additional BECMI or compatible reference material.

These stages may also introduce richer monster variants and special rules.

### Canonical Definitions

Canonical definitions are the game's authoritative definitions for monsters, characters, equipment, spells, and other game entities.

External sources are inputs used to create these definitions; they are not runtime dependencies.

### Instantiate

Create individual runtime entities from canonical definitions.

Instantiation resolves values that can vary between individuals, such as hit points, equipment, treasure, and other runtime state.

### Runtime State

Runtime objects contain mutable state such as current hit points, temporary adjustments, conditions, inventory changes, and encounter state.

Runtime changes must not modify canonical definitions.

### Rules Engine

The rules engine operates on canonical definitions and runtime state to resolve combat and other game mechanics.

It should depend on the game's internal model rather than external source formats.

## Design Principles

- **RC/BECMI is the primary rules foundation.** OSE is a compatible data source.
- **Store state; calculate derived values.**
- **Separate static definitions from mutable runtime instances.**
- **External source formats should not leak into the rules engine.**
- **Preserve source data when implementation of an edge case is intentionally deferred.**
- **Prefer requirements-driven abstractions over premature generalization.**
- **Keep core game rules framework-independent.** Persistence and multiplayer systems should integrate with the rules engine rather than define it.

## Current Direction

```text id="drj7uw"
OSE Import / Validation
        ↓
OSE Normalization        ← Current
        ↓
Stabilize Monster Model
        ↓
Enrichment / Variants
        ↓
Canonical Definitions
        ↓
Runtime Instantiation
        ↓
Encounter Resolution
        ↓
Persistence / Multiplayer
```

Detailed schemas, normalization rules, house rules, and source-specific behavior are documented separately under `docs/`.