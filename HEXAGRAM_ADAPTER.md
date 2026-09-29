# Hexagram snapshot — adapter only

DebugShrine does not ship a 64-hexagram generator.

Snapshot = optional compressed image of an already computed surface.  
Not a class. Not an audit verdict.

## Proposal

Customize an **existing** I Ching / hexagram tool (library, table, or app you already trust).

Feed it only derived, non-authoritative inputs:

```yaml
input_allowed:
  - total
  - dominant_edge
  - dominant_ratio
  - surface          # Stable | Emerging | Locked
input_forbidden:
  - invented gate myths
  - class overrides
  - unpublished weights presented as spec
```

## Responsibility

```text
Weighting = operator
Operation = operator
Interpretation = operator
```

GitHub DebugShrine accepts the tool’s string back into `Snapshot` as opaque text.

If the tool is wrong, the records still stand. Rebuild surface from points.
