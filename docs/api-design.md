# RiskLedger API Design (Phase 1)

Design only. Nothing here is implemented yet; each endpoint gets built in a later lesson.

## Conventions

- JSON request and response bodies.
- IDs are integers in the path.
- Errors: `404` for an unknown ID, `422` for a body that fails validation.
- List endpoints support `limit` and `offset` query parameters.

## Vendors

| Method | Path | Purpose | Success |
|--------|------|---------|---------|
| GET | `/vendors` | List vendors (supports `limit`, `offset`) | 200 |
| GET | `/vendors/{id}` | Get one vendor | 200 |
| POST | `/vendors` | Create a vendor | 201 |
| PATCH | `/vendors/{id}` | Partially update a vendor | 200 |
| DELETE | `/vendors/{id}` | Delete a vendor (and its findings) | 204 |

**PATCH, not PUT:** clients usually change one field (e.g. risk tier), and PATCH lets them send only that field instead of the whole record.

## Findings

Findings belong to a vendor, so listing and creating are nested under the vendor. Operating on a single finding uses a flat path, since its ID is already unique.

| Method | Path | Purpose | Success |
|--------|------|---------|---------|
| GET | `/vendors/{id}/findings` | List findings for a vendor | 200 |
| POST | `/vendors/{id}/findings` | Create a finding for a vendor | 201 |
| GET | `/findings/{id}` | Get one finding | 200 |
| PATCH | `/findings/{id}` | Partially update a finding (e.g. status) | 200 |
| DELETE | `/findings/{id}` | Delete a finding | 204 |

Note: `GET /vendors/{id}/findings` and `POST /vendors/{id}/findings` return `404` if the vendor does not exist.
