# RFC 9110 Crosswalk (Informative)

This document is an informational crosswalk only.

It does not define, imply, or claim RFC 9110 compliance for any
DebugShrine classification behavior.

RFC 9110 defines HTTP semantics.

DebugShrine defines its own observational classifications
(Class, RouteError, Surface).

No DebugShrine classification is derived from, required by,
or equivalent to any RFC 9110 method, status code, routing rule,
or protocol element.

The mappings in this document are provided only to explain
boundary decisions and prevent terminology confusion.

Non-equivalence guarantees:

```
404 != BOUNDARY
500 != GOVERNANCE
POST != GOVERNANCE
GET != NORMAL
HTTP routing != RouteError
```

Compact four-column form (safe to quote):

| RFC | Element | RFC requirement | DebugShrine |
|-----|---------|-----------------|-------------|
| §15.5 | 4xx / 404 | status-code semantics | not used as Class |
| §15.6 | 5xx / 500 | status-code semantics | not used as Class |
| §9.3.1 | GET | method semantics | not used as Class |
| §9.3.3 | POST | method semantics | not used as Class |
| §7 | Routing | target-resource routing | independent of RouteError |

---


Source: [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) (STD 97, June 2022)  
Purpose: Grok-link / public FAQ later — **not** a claim that DebugShrine implements RFC 9110.

Two layers stay distinct:

| Layer | What it is |
|-------|------------|
| RFC 9110 | HTTP method, status, field, message semantics |
| DebugShrine | Record → aggregate → classify (`GOVERNANCE\|BOUNDARY\|NORMAL`) |

RFC 9110 never defines those three classes.  
DebugShrine never redefines HTTP status.

---

## How to read the table

- **RFC says** = paraphrase of that section’s job, not a substitute for the text.
- **DebugShrine bind** = what the public method does if an HTTP message is an *ingress adapter*.
- **MUST/MAY** in the last column are **DebugShrine policy**, not RFC 2119 words from 9110 unless marked `9110:`.

---

## Crosswalk

| RFC 9110 | Title (as in the RFC) | RFC says | DebugShrine bind | Policy |
|----------|----------------------|----------|------------------|--------|
| 1 | Introduction / architecture | Uniform interface; request/response; semantics shared by HTTP/1.1, /2, /3 | Ingress may be any HTTP version; Class does not encode the version | MUST NOT classify by protocol version |
| 1.3 | Core operations | Client intent in request; server result in status + content | Intent field is application text, not the HTTP method token | MAY store method as metadata |
| 2.2 | Conformance | Roles: client, server, intermediary | DebugShrine is not an HTTP participant; it is a notebook after the fact | n/a |
| 3.1 | Resources | Target resource identified by URI | URI MAY be stored on Record; URI is not ExpectedGate | MAY |
| 3.2 | Representations | Payload + metadata | Representation is not Surface | MUST NOT derive Surface from body |
| 3.4–3.7 / 6 | Messages, methods, status, fields (concepts) | A message has method or status + fields | Those elements are observations if logged | MAY copy, MUST NOT classify from them alone |
| 5 | Fields | Header/trailer fields are metadata | Fields MAY be Notes / extra JSON; additionalProperties allowed | MUST NOT change Class |
| 7 | Routing HTTP messages | Intermediaries forward; routing is HTTP routing | HTTP routing ≠ DebugShrine RouteError | MUST: RouteError = ExpectedGate ≠ ActualGate only |
| 9 | Methods | GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE (+ extensions) | Method does not select GOVERNANCE / BOUNDARY / NORMAL | MUST NOT |
| 9.2 | Method properties (safe / idempotent) | Safe/idempotent are HTTP properties | Not GovernanceFlag | MUST NOT map safe→NORMAL or POST→GOVERNANCE |
| 15 | Status codes | 1xx–5xx meaning for HTTP recipients | Status is not Class | MUST NOT |
| 15.5 | Client error 4xx | e.g. 404 Not Found | 404 ≠ BOUNDARY | MUST NOT |
| 15.6 | Server error 5xx | e.g. 500 | 500 ≠ GOVERNANCE | MUST NOT |
| 16 | Extending HTTP | New methods/status/fields via registry | Extensions still HTTP metadata | same as §5 / §9 / §15 |
| 17 | Security considerations | HTTP-layer attacks | Out of DebugShrine method contract | OPS only if ever |

---

## Explicit non-mappings

Do not publish these equivalences:

```
404          ≠  BOUNDARY
500          ≠  GOVERNANCE
POST         ≠  GOVERNANCE
GET          ≠  NORMAL
Host/route   ≠  RouteDelta
HTTP 5xx     ≠  Freeze / override
```

Tests that lock the non-mapping live in `tests/test_schema.py`
(`HttpStatus` extra field, Class unchanged).

---

## When a Grok link needs this file

Use this document to answer:

> “You mention RFC 9110 — does DebugShrine comply with section X?”

Answer template:

```
RFC 9110 §X defines HTTP element E.
DebugShrine may store E on a Record (MAY).
DebugShrine Class / RouteError / Surface are not functions of E (MUST NOT).
Compliance with §X is an HTTP implementation concern, not this repo.
```

---

## What this file is not

- Not a 9110 profile
- Not a requirement matrix for HTTP servers
- Not OPS / product RFC catalogs
- Not a substitute for the RFC text

Canonical RFC: https://www.rfc-editor.org/rfc/rfc9110.html  
Info page: https://www.rfc-editor.org/info/rfc9110
