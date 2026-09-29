# Contributing

Thank you for your interest in DebugShrine.

## Scope

This repository publishes a public contract:

- schemas
- validators
- release checks
- tests
- documentation

Private operational components are intentionally excluded.

## Guiding principle

Keep three layers distinct:

1. RFC semantics
2. DebugShrine concepts
3. User interpretations

Do not introduce implicit equivalence between these layers.

## Acceptable

- bug reports
- documentation fixes
- test improvements
- schema validation improvements
- boundary clarifications

## Discuss first (open an issue)

- behavioral changes
- classification changes
- schema-breaking changes
- public contract changes
- release gate changes

## RFC references

RFC references may be used for explanation.

Do not add mappings that imply:

- HTTP status ↔ Class
- HTTP method ↔ Class
- HTTP routing ↔ RouteError

Crosswalk documents are informative only.

## O-mikuji

Narrative presentation layer only.

Do not represent O-mikuji as fortune telling, prediction,
decision support, or risk assessment.

## Pull requests

- pass CI
- pass `python tools/release_check.py`
- keep docs consistent with the public/private boundary

## License

Contributions are licensed under the same license as the repository (MPL-2.0).
