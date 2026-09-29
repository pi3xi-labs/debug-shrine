# DebugShrine

DebugShrine is an observational classification experiment.

This repository publishes a minimal public contract:

- schema
- validation logic
- release checks
- tests
- documentation

Intended public URL: https://github.com/pi3xi-labs/debug-shrine

## Public Boundary

Included:

- classification schema
- validators
- release gate
- CI configuration
- documentation

Not included:

- operational rules
- gate dictionaries
- local deployment code
- inference engines
- private workflows

The absence of a component from this repository does not imply
that the component does not exist. It means it is not published here.

## What This Repository Is Not

- an HTTP framework
- an RFC 9110 classification system
- a routing engine
- a decision-support system
- a risk-assessment system
- a prediction system
- a fortune-telling system

## RFC 9110 Boundary

RFC 9110 defines HTTP semantics.

DebugShrine defines independent observational concepts.

Non-equivalence guarantees:

- 404 != BOUNDARY
- 500 != GOVERNANCE
- GET != NORMAL
- POST != GOVERNANCE
- HTTP routing != RouteError

Any RFC 9110 crosswalk is informational only.
See `docs/RFC9110_CROSSWALK.md`.

## O-mikuji

O-mikuji is a narrative view of a snapshot.

It is not fortune telling, prediction, decision support, or risk assessment.

Do not use O-mikuji outputs for personal, financial, legal, medical,
or operational decisions.

One line: *O-mikuji is a narrative view of a snapshot, not a prediction.*

## FAQ

**Is BOUNDARY HTTP 404?**  
No.

**Is GOVERNANCE HTTP 500?**  
No.

**Do GET or POST determine Class?**  
No.

**Is RouteError HTTP routing?**  
No.

**Does this repository claim RFC 9110 compliance for classification?**  
No. Crosswalk is informative only.

**Why provide a crosswalk?**  
To explain boundaries and prevent terminology confusion.

Longer answers: `docs/FAQ.md`.

## Observation Metrics

Public discussion may introduce interpretations that differ from
the documented contract.

See `docs/metrics.csv`.

The metrics are observational only.
They are not quality scores, user scores, or compliance indicators.

Watch especially: F4 (fortune misread), N3 (character completion),
R1 (RFC contamination), B4 (absence read as nonexistence).

## CLI

```bash
python tools/build_hogan.py
python tools/gitops.py snapshot
python tools/release_check.py
pytest -q
```

## License

Mozilla Public License 2.0. See `LICENSE` and `NOTICE`.

Copyright (c) 2026 pi3xi-labs / wizyig  
(holder string adopted for this public pack)

## Contributing

See `CONTRIBUTING.md`.

Keep three layers distinct:

```
RFC semantics
≠ DebugShrine concepts
≠ user interpretation
```
