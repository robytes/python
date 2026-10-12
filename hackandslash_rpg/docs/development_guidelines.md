# Hack-and-Slash RPG Agent Instructions

This project is a Python RPG engine based primarily on D&D Rules
Cyclopedia / BECMI, with OSE used as a compatible external data source.

## Authority

When determining project behavior, prefer:

1. Current source code
2. Explicit decisions under `docs/`
3. These project instructions
4. Conversation context

Do not assume exploratory or historical designs are current when they
conflict with the repository.

## Development Approach

- Prefer straightforward Python.
- Avoid premature abstraction.
- Let actual game requirements drive architecture.
- Preserve boundaries between source data, normalization, derivation,
  enrichment, canonical definitions, and runtime state.
- Do not redesign established architecture without explaining why.

## Interactive Coaching

This project is also used to improve Python skills.

For learning-oriented work:
- Let the developer attempt the implementation first.
- Use progressively stronger hints.
- Explain relevant Python behavior.
- Break complex problems into small steps.
- Review completed code for correctness and readability.

For repetitive work such as documentation cleanup, data inspection,
or mechanical refactoring, direct solutions are appropriate.

## Documentation

Read relevant files under `docs/` before making architectural changes.

Do not treat unresolved or provisional fields as established design.