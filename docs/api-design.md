# RiskLedger API Design (Phase 1)

Design only unless marked "built". Each endpoint is implemented in a later lesson.

## Conventions

- JSON request and response bodies.
- Plural nouns, no verbs in paths, no trailing slashes.
- IDs are integers in the path.
- Errors: `404` for an unknown ID, `422` for input that fails validation.
- List endpoints support `limit` and `offset` query parameters.
- **Route order:** static paths (`/vendors/summary`, `/findings/open`) are declared
  before parameterised paths (`/vendors/{id}`, `/findings/{id}`). The router matches
  in declaration order; the reverse would route "summary" into `{id}` and return 422.

## Vendors

| Method | Path | Purpose | Success | State |
|--------|------|---------|---------|-------|
| GET | `/vendors` | List vendors (supports `limit`, `offset`) | 200 | built |
| GET | `/vendors/summary` | Counts by tier and active vendors | 200 | built |
| GET | `/vendors/{id}` | Get one vendor | 200 | |
| POST | `/vendors` | Create a vendor | 201 | |
| PATCH | `/vendors/{id}` | Partially update a vendor | 200 | |
| DELETE | `/vendors/{id}` | Offboard a vendor (soft delete: status = offboarded) | 204 | |

**PATCH, not PUT:** clients usually change one field (e.g. risk tier); PATCH sends only that field.

**Soft delete:** risk and audit records must keep their history, so DELETE marks a vendor
offboarded instead of erasing it and its findings.

## Findings

Findings belong to a vendor, so listing and creating are nested under the vendor.
Operating on a single finding uses a flat path, since its ID is already unique.

| Method | Path | Purpose | Success | State |
|--------|------|---------|---------|-------|
| GET | `/findings` | List all findings | 200 | built |
| GET | `/findings/open` | Open findings, highest CVSS first | 200 | built |
| GET | `/vendors/{id}/findings` | List findings for a vendor | 200 | |
| POST | `/vendors/{id}/findings` | Create a finding for a vendor | 201 | |
| GET | `/findings/{id}` | Get one finding | 200 | |
| PATCH | `/findings/{id}` | Partially update a finding (e.g. status) | 200 | |
| DELETE | `/findings/{id}` | Delete a finding | 204 | |

`GET /vendors/{id}/findings` and `POST /vendors/{id}/findings` return `404` if the vendor does not exist.