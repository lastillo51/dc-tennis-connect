# DC Tennis Connect — Project Requirements

> **Phase 8 Exercise 6 review:** 2026-11-25. This document replaces a misfiled copy of the feature backlog in the supplied repository snapshot. The backlog remains in `feature-backlog.md`. Phase 8 merge and public deployment are not yet approved.

## 1. Purpose and product boundaries

DC Tennis Connect helps Washington, D.C. tennis players find court facilities, inspect published information, and navigate with Google Maps. A future voluntary community scheduling service will let participants coordinate court time without claiming official DPR reservation rights. It does not guarantee physical occupancy, priority over nonparticipants, or public access.

## 2. Users and scope

- Recreational tennis players discovering courts and seeking directions.
- Future participating players scheduling community time slots and coordinating matches.
- Project maintainers validating and importing authorized public court information.

The current implementation is local development only. Player accounts, scheduling, notifications, QR codes and public cloud hosting remain future features.

## 3. Functional requirements

| ID | Requirement | Phase 8 status / acceptance |
|---|---|---|
| FR-001 | List court facilities from persistent data | Implemented: FastAPI `/courts/` and `/web/courts` use SQLAlchemy-backed service |
| FR-002 | Search by name/address and filter public access | Implemented: query validation and shared service |
| FR-003 | Show facility detail, reported court count and location | Implemented for stored records; real DPR publication pending |
| FR-004 | Open Google Maps directions from validated court location | Implemented with fixed HTTPS Google Maps host and encoded destination |
| FR-005 | Show unknown official reservation policy explicitly | Implemented: nullable `reservation_required`, API `null`, frontend “Unknown” |
| FR-006 | Track source attribution and stable external identity | Schema implemented: `court_sources`, `source_identifier`, unique namespace identity |
| FR-007 | Validate authorized public GIS data before import | Implemented: Pydantic DC GIS Layer 9 adapter and dry-run classification |
| FR-008 | Require explicit reviewed public-access approval for real publication | Partial: manifest validation and test-only apply; independent approval and provenance persistence pending |
| FR-009 | Record verified operating hours, closures and restrictions | Planned; do not invent unknown hours or interpret status as physical availability |
| FR-010 | Create and cancel voluntary community court reservations | Planned; not an official DPR reservation |
| FR-011 | Prevent overlapping community bookings for each schedulable court unit | Planned; multi-court facilities require distinct units |
| FR-012 | Display voluntary booking disclaimer and applicable facility rules | Planned; bookings do not guarantee court availability |
| FR-013 | Offer QR-code links to community court schedules | Planned; court-site posting requires appropriate permissions |
| FR-014 | Support player profiles and hitting partner coordination | Planned |

## 4. Data requirements

- Persist `courts` and `court_sources` with PostgreSQL 17, SQLAlchemy and versioned Alembic migrations.
- Maintain constraints on court counts, coordinate ranges, availability classifications and source relationships.
- Represent unknown official reservation policy as `NULL`; do not infer `FALSE`.
- Maintain unique `(source_name, source_identifier)` for non-null source identifiers, while separately reviewing cross-source facility duplicates.
- Record genuine source and approval evidence, verification time and change history before publishing real records; the current importer does not yet persist approval evidence.
- Keep fictional test fixtures isolated from approved real records.

## 5. Security and nonfunctional requirements

- Keep database credentials outside Git, use environment configuration and least-privilege access.
- Validate and escape untrusted browser and GIS inputs; construct Google Maps links with a fixed trusted host.
- Require explicit target confirmation, reviewed backups and migration testing before schema changes on valuable databases.
- Default import tooling to read-only; test-only apply remains restricted to `dc_tennis_test` until approval and safety controls are completed.
- Run database-enabled integration tests locally and CI-compatible tests without PostgreSQL; preserve regression coverage.
- Maintain responsive, accessible HTML and safe, understandable errors.
- Do not claim real-time occupancy, official reservation authority or production readiness.

## 6. Current acceptance and release boundaries

Phase 8 infrastructure acceptance covers working database connectivity, ORM/repository integration, three Alembic migrations through `61174a56cf41`, API/frontend regression tests, DC GIS source validation, read-only import planning and isolated test-only transactional inserts. The 50 DPR candidates / 148 reported courts have not been imported or approved for publication. Final security evidence, documentation review, PR and merge remain outstanding.

## 7. Related documents

- `docs/requirements/feature-backlog.md` — prioritization and delivery status
- `docs/architecture/system-overview.md`
- `docs/architecture/database-overview.md`
- `docs/security/security-policy.md`
- `docs/runbooks/security-findings.md`
- `docs/runbooks/repository-snapshot-management.md`