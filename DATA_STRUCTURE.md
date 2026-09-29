# Excel 方眼紙データ構造

File: `DebugShrine_PUBLIC_v1.0.1_hogan.xlsx`  
Grid unit: one cell = one observation slot or one derived slot.  
Blue font = input. Black font = formula. Yellow fill = operator-editable assumption.

---

## Sheet map

```
00_COVER      metadata, not a table
01_FLOW       6 rows × 6 cols integration matrix
02_RECORD     N rows × 12 cols  ← canonical table
03_PALACE9    3×3 bins keyed by ActualGate ∈ {1..9}
04_SURFACE    scalars + spilled edge table + chart source
05_CLASS      3-row truth table
06_ADAPTER    5-row hook
```

Print: every sheet A4 landscape, fitToPage 1×1, header = sheet name, footer = page + disclaimer.

---

## 02_RECORD  (canonical)

Header row = 3. Data starts row 4. Filter `A3:L22`. Freeze `A4`.

| Col | Name | Excel type | Origin | Formula (row r) |
|-----|------|------------|--------|-----------------|
| A | RecordId | text | input | |
| B | Timestamp | text | input | |
| C | Turn | text | input | |
| D | Intent | text | input | |
| E | ExpectedGate | text/number | input | |
| F | ActualGate | text/number | input | |
| G | GovernanceFlag | bool / list TRUE,FALSE | input | validation G4:G22 |
| H | RouteError | bool | derived | `=IF(OR(E{r}="",F{r}=""),"",E{r}<>F{r})` |
| I | RouteDelta | text | derived | `=IF(OR(E{r}="",F{r}=""),"",E{r}&"→"&F{r})` |
| J | Class | text | derived | `=IF(G{r}="","",IF(G{r}=TRUE,"GOVERNANCE",IF(H{r}=TRUE,"BOUNDARY","NORMAL")))` |
| K | Notes | text | input | |
| L | Valid | text | derived | OK if Class matches flags; WAIT if incomplete |

Conditional format on J:

- GOVERNANCE → red fill
- BOUNDARY → amber fill
- NORMAL → green fill

Rows 4–13: sample (disposable).  
Rows 14–22: empty yellow input slots.

Logical PK = RecordId.  
Do not use Class as PK.

---

## 03_PALACE9

Visual 3×3. Each bin:

| Visual | Label cell | Count cell |
|--------|------------|------------|
| NW | `cell 1` | `=COUNTIF('02_RECORD'!F4:F22,"1")` |
| N  | `cell 2` | COUNTIF … "2" |
| NE | `cell 3` | "3" |
| W  | `cell 4` | "4" |
| C  | `cell 5` | "5" |
| E  | `cell 6` | "6" |
| SW | `cell 7` | "7" |
| S  | `cell 8` | "8" |
| SE | `cell 9` | "9" |

If ActualGate is `A`/`B`/`C`, all bins stay 0. That is correct for the sample.  
Bins are storage boxes, not a cosmology.

---

## 04_SURFACE

| Cell | Name | Formula / value |
|------|------|-----------------|
| B3 | total | `=COUNTA('02_RECORD'!E4:E22)` |
| B4 | distinct_edges | `SUMPRODUCT` uniqueness over I4:I13 |
| B5 | STABLE_LT | **0.35** (input, yellow) |
| B6 | LOCKED_GE | **0.60** (input, yellow) |
| M4:M22 on 02_RECORD | EdgeFreq | `COUNTIF($I$4:$I$22,I{r})` |
| B9 | count | `=COUNTIF('02_RECORD'!I4:I22,A9)` |
| C9 | ratio | `=B9/$B$3` |
| B19 | max_count | `=MAX('02_RECORD'!M4:M22)` |
| B20 | dominant_ratio | `=IF(B3=0,0,B19/B3)` |
| B21 | Surface | `=IF(B3=0,"",IF(B20<B5,"Stable",IF(B20<B6,"Emerging","Locked")))` |

Chart source `E3:F6`:

| Class | n |
|-------|---|
| GOVERNANCE | `COUNTIF(J:J,"GOVERNANCE")` |
| BOUNDARY | COUNTIF … |
| NORMAL | COUNTIF … |

Bar chart category = Class, values = n, y-min = 0.

UNIQUE/FILTER is not used. Sample 10 rows → A→B count 6 → ratio 0.60 → Locked.

---

## 05_CLASS

Static normative table. Not computed.

| GovernanceFlag | RouteError | Class |
|----------------|------------|-------|
| TRUE | any | GOVERNANCE |
| FALSE | TRUE | BOUNDARY |
| FALSE | FALSE | NORMAL |

---

## 06_ADAPTER

| Row | Label | Binding |
|-----|-------|---------|
| 7 | Surface | `='04_SURFACE'!B21` |
| 8 | dominant_ratio | `='04_SURFACE'!B20` |
| 9 | Snapshot | input paste |
| 10 | Tool name / version | input |
| 11 | Operator accepts weights | bool input, default FALSE |

No formula produces a hexagram.

---

## 01_FLOW columns

`段 | 主体 | 入力 | 処理 | 出力 | 禁止`

Six stages: Ingress, Record, Aggregate, Compress, Classify, Egress.

---

## Integrity rules implemented in-sheet

```
V1 ExpectedGate present
V2 ActualGate present
V3 RouteDelta = Expected→Actual
V4 Class=GOVERNANCE iff GovernanceFlag
V5 Class=BOUNDARY iff not Flag and RouteError
V6 Class=NORMAL iff not Flag and not RouteError
V8 Surface only if total>0
```

V7 (snapshot after total>0) is operational, checked by hook emptiness.

---

## Serialization

Python dataclass `AuditRecord` ↔ sheet row ↔ JSONL line are 1:1 on columns A–G (inputs) plus derived H–J.

Git snapshot recommended paths:

```
out/records.jsonl
out/aggregate.json
out/DebugShrine_PUBLIC_v1.0.1_hogan.xlsx
```
