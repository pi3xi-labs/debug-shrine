# DebugShrine PUBLIC v1.0

GitHub-facing method contract.  
Aggregation + classification + external I/O.  
No local code catalog. No hexagram generator.

Status: PUBLIC COMPLETE  
Date: 2026-09-30  
Not: product map

---

## 1. Law

```
Observe → Record → Aggregate → Compress(hook) → Classify
```

Direction: point → surface only.

Logger does not classify.  
Snapshot is not a verdict.  
Local names bind after this spec, never inside it.

---

## 2. Record (ingress)

```yaml
AuditRecord:
  RecordId: string
  Timestamp: string
  Turn: string
  Intent: string
  ExpectedGate: scalar
  ActualGate: scalar
  GovernanceFlag: boolean
```

Derived:

```yaml
RouteError: ExpectedGate != ActualGate
RouteDelta: ExpectedGate → ActualGate
```

Gates are opaque. This spec has no gate dictionary.

---

## 3. Classify

```
GOVERNANCE  if GovernanceFlag
BOUNDARY    else if RouteError
NORMAL      else
```

Priority: GOVERNANCE wins when both readings are possible.  
Schema: `public/classification.schema.json` (`oneOf`).

---

## 4. Aggregate

```
node[actual] += 1
edge[expected → actual] += 1
dominant_ratio = max(edge) / sum(edge)
```

Surface:

| Band | Ratio |
|------|--------|
| Stable | < 0.35 |
| Emerging | [0.35, 0.60) |
| Locked | ≥ 0.60 |

Empty trajectory → no surface.

---

## 5. Compress (hook only)

```yaml
Snapshot:
  input: trajectory + surface
  output: opaque image (string | object)
  authority: none
  generator: NOT IN THIS REPO
```

GitHub DebugShrine ships the hook, not a 64-hexagram engine.  
See `HEXAGRAM_ADAPTER.md`.

---

## 6. External integration

### Ingress adapters (allowed)

| Source | Maps to |
|--------|---------|
| NDJSON / YAML log | AuditRecord |
| HTTP POST /record | AuditRecord |
| Spreadsheet row | AuditRecord |
| CI annotation | AuditRecord |

Adapter duty: copy fields. Do not invent Class or Surface.

### Egress (allowed)

| Sink | Payload |
|------|---------|
| JSONL audit log | records + derived Route* |
| Aggregate file | node_count, edge_count, ratio, surface |
| Classification file | Class per record |
| Snapshot slot | passthrough from external tool |
| Spreadsheet 方眼紙 | same columns |

### Forbidden on the wire

- sending Class as an observation
- sending Surface as a logger field
- embedding a hexagram as input to classify
- product RFC / boundary codes in public payloads

### Minimal POST body

```json
{
  "RecordId": "REC_001",
  "Timestamp": "2026-09-30T00:00:00Z",
  "Turn": "T1",
  "Intent": "review",
  "ExpectedGate": "A",
  "ActualGate": "B",
  "GovernanceFlag": false
}
```

### Minimal aggregate response

```json
{
  "total": 10,
  "dominant_ratio": 0.8,
  "surface": "Locked",
  "edges": { "A->B": 8, "A->A": 2 }
}
```

---

## 7. Data flow

```
[external logger / CI / sheet]
        |  AuditRecord
        v
   DebugShrine Record store
        |  facts only
        +--> classify()     --> Class
        +--> aggregator     --> Surface
        +--> snapshot hook  --> external tool --> opaque image
        v
   egress JSONL / Excel / Git artifact
```

Recompute is always from records. Downstream files are disposable.

---

## 8. Local-code generation function

Public spec does **not** generate local codes.

```yaml
local_code = bind(Class, consumer_catalog)
```

- Class is public (`GOVERNANCE|BOUNDARY|NORMAL`)
- consumer_catalog is outside this repo
- bind() is the consumer’s function
- DebugShrine never emits product codes / palace-cell ids

If a consumer needs a code:

```
record + Class  -->  consumer.bind()  -->  local_code
```

Not the reverse.

---

## 9. Closure (GitHub version)

Complete when:

- I/O and flow are specified
- classify + aggregate are specified
- snapshot is a hook
- local codes stay outside
- Excel 方眼紙 is a view, not an oracle

Not in GitHub DebugShrine:

- 64-hexagram weighting
- palace-to-gate map
- operational catalogs
