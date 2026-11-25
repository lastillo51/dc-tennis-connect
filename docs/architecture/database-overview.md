# DC Tennis Connect — Database Architecture

> **Phase 8 Exercise 6 current-state review (2026-11-25; source snapshot `21e53c4534bd989ff1df5c7422960b85cd9f30b8`).** The sections below record the implemented Phase 8 state. Older planning/checkpoint sections retained later in this file are historical and must not be read as the current implementation status. This update is prepared for review on `feature/postgresql-court-data`; no merge into `main` is asserted.

## Phase 8 Exercise 6 — Verified implementation and remaining scope

- **Implemented in the supplied repository:** PostgreSQL 17 Docker Compose persistence; SQLAlchemy/Psycopg sessions and ORM; Alembic revisions `70a0a04f5a58` → `b83f1c2d9a60` → `61174a56cf41`; PostgreSQL-backed court service, JSON API and Jinja2 pages; Google Maps directions; DC GIS Layer 9 validation, source-identity comparison, dry-run CLI, approval manifest and test-only import command.
- **Data source evaluation (reported during Exercise 5):** 50 DPR candidate properties, 148 source-reported courts, 49 marked active and one with unknown active status (Oxon Run Park, `DPR_0501`). These are candidate/source counts, **not** imported, verified-open, or physically available courts. The JSON download is local and excluded from the Git archive.
- **Not complete:** real DPR record publication; independently verified access and hours for all candidates; persisted approval evidence and verification timestamps for imported records; cross-source duplicate reconciliation; safe updates and production import authorization; player accounts; voluntary community scheduling and QR-code adoption.
- **Scheduling policy:** Future bookings will be voluntary commitments managed by DC Tennis Connect, independent of official DPR reservation systems. They confer no exclusive right to a court and cannot guarantee occupancy or availability. Unknown official reservation requirements remain `NULL` and display as “Unknown.”
- **Release boundary:** Local development only. Exercise 6 documentation, security verification, PR review and merge remain pending.


**Current phase:** Phase 8 — Exercise 6 (final review)  
**Implementation status:** PostgreSQL-backed application retrieval and three Alembic revisions implemented; dry-run and test-only import infrastructure implemented; real public court publication and merge pending.

## 1. Purpose and boundaries

Introduce PostgreSQL-backed public tennis court information without breaking the Phase 7 FastAPI JSON API, Jinja2 pages, court service, or Google Maps directions. This phase does not implement player accounts, official court reservations, or real-time court occupancy.

The PostgreSQL schema is operational and court retrieval is integrated through the repository and mapper. Verified real court imports remain planned for Exercise 5.

## 2. Implemented technology

| Component | Technology | Current role and status |
|---|---|---|
| Persistence | PostgreSQL 17 | Running in Docker Compose with persistent storage; initial tables created |
| Data access | SQLAlchemy 2.x | Engine, session factory, declarative models and metadata implemented |
| Driver | Psycopg 3 | Host-to-container database connectivity verified |
| Schema migrations | Alembic | Initial revision `70a0a04f5a58` applied and validated |
| Tests | Pytest | Connectivity, constraints, ORM metadata, migration structure and schema tests |
| Local runtime | Docker Compose | `db` service healthy; PostgreSQL host port bound to localhost |

Dependencies are recorded in `requirements.txt`; versions should be taken from that file rather than assumed from this document. The original Exercise 1 proposal has been superseded by the verified Exercises 2–3 implementation.

## 3. Data access flow

**Current application flow:** Browser / JSON client → FastAPI routes → shared court service → SQLAlchemy repository → PostgreSQL.

**Implemented database foundation:** SQLAlchemy engine and `SessionLocal` in `app/db/session.py` → Psycopg 3 → PostgreSQL; Alembic manages schema changes.

**Implemented Exercise 4 application flow:** Browser / JSON client → FastAPI web/API routes → shared court service → SQLAlchemy repository → PostgreSQL.

The service maps persistent records to the existing Pydantic `Court` schema. Templates must not query PostgreSQL. The existing Maps service derives fixed-host Google Maps URLs from validated locations.

## 4. Initial entities — implemented schema

### `courts`

| Field | PostgreSQL type | Implemented constraint or behavior |
|---|---|---|
| `id` | INTEGER primary key | Database-generated integer key; positive IDs enforced by API schema, not a DB check |
| `name` | VARCHAR(100) | `NOT NULL`; nonempty content requires application validation |
| `address` | VARCHAR(200) | `NOT NULL`; nonempty content requires application validation |
| `latitude` | DOUBLE PRECISION | Nullable; check between -90 and 90 |
| `longitude` | DOUBLE PRECISION | Nullable; check between -180 and 180 |
| `number_of_courts` | INTEGER | `NOT NULL`; check at least 1 |
| `public_access` | BOOLEAN | `NOT NULL` |
| `availability_status` | VARCHAR(40) | `NOT NULL`; default `unknown`; controlled values |
| `reservation_required` | BOOLEAN | Nullable; no server default; `NULL` means official policy unknown |
| `created_at` | TIMESTAMPTZ | `NOT NULL`; database default `now()` |
| `updated_at` | TIMESTAMPTZ | `NOT NULL`; database default `now()`; SQLAlchemy-side `onupdate` |

The approved availability values are `published_hours`, `reservable`, `first_come_first_served`, `closed`, and `unknown`.

The `updated_at` field is not automatically changed by arbitrary direct SQL updates; a trigger would be required for database-enforced updates.

### `court_sources`

| Field | PostgreSQL type | Implemented constraint or behavior |
|---|---|---|
| `id` | INTEGER primary key | Database-generated integer key |
| `court_id` | INTEGER foreign key | `NOT NULL`; references `courts.id`, `ON DELETE CASCADE`; indexed |
| `source_name` | VARCHAR(150) | `NOT NULL`; together with non-null `source_identifier` forms unique source identity |
| `source_identifier` | VARCHAR(200) | Nullable; unique with `source_name` for non-null values |
| `source_url` | VARCHAR(1000) | `NOT NULL`; URL scheme/host validation not enforced by DB |
| `source_type` | VARCHAR(40) | `NOT NULL`; controlled category |
| `last_verified_at` | TIMESTAMPTZ | Nullable in initial schema |
| `created_at` | TIMESTAMPTZ | `NOT NULL`; database default `now()` |

The approved source types are `official`, `open_data`, `reservation_platform`, and `other`.

**Historical differences from Exercise 1 proposal (superseded by later migrations):** The implemented model uses `source_name`, not `publisher`; `source_url` is `VARCHAR(1000)`, not `TEXT`; `source_identifier` is not yet implemented; `last_verified_at` is nullable; `source_type` is `VARCHAR(40)`. These are deliberate descriptions of the actual migration, not claims that the original proposal was implemented verbatim.

A court may have multiple source records. Stable upstream source identity is implemented; cross-source facility reconciliation, approval evidence persistence, operating hours, closures and restrictions remain pending.

## 5. Data integrity and import

Implemented database checks protect court counts, coordinate ranges, controlled classifications, non-null fields, and court-source referential integrity. Application-level validation must also enforce meaningful names, addresses, URL policy, source provenance, positive identifiers, and real-record freshness.

Before Exercise 5 imports:

- Confirm authorized access and reuse of each public source.
- Require source attribution and verification timestamps for imported real records.
- Validate addresses, counts, coordinates, classifications, and dates.
- Define stable duplicate-detection keys and idempotent imports.
- Keep fictional fixtures separate from real court records.
- Distinguish published operating hours from reservations and physical occupancy.
- Log import failures without exposing secrets.

### Exercise 5 ingestion architecture

`app/importers/dcgis_adapter.py` validates saved ArcGIS Layer 9 JSON; `schemas.py` represents candidate properties with unknown public access and reservation policies; `repository.py` loads existing identities read-only; `planner.py` classifies actions; `scripts/import_public_courts.py` enforces a read-only comparison on approved disposable databases. The approval manifest is empty. `scripts/apply_public_courts.py` is restricted to `dc_tennis_test`; `service.py` stages insert-or-skip records in a caller-owned transaction and does not implement approved updates. It does not persist the manifest's evidence URL/verification time. Do not describe this as production-ready or a real-data import.

### Migration sequence (current)

| Revision | Change |
|---|---|
| `70a0a04f5a58` | Initial `courts` and `court_sources` schema |
| `b83f1c2d9a60` | Nullable `source_identifier` and `(source_name, source_identifier)` uniqueness |
| `61174a56cf41` | Nullable `reservation_required` and removal of the false server default |

The nullable-policy downgrade maps `NULL` to `FALSE`, losing the unknown state. Only exercise downgrade on disposable databases, not on valuable records.

## 6. Migrations and rollback

Alembic revision `70a0a04f5a58` creates `courts`, `court_sources`, their constraints, foreign key, and source lookup index. The `alembic_version` table tracks the applied revision.

The initial migration was applied to the normal development database. `alembic current`, `alembic heads`, and `alembic check` verified revision alignment and no outstanding autogenerated schema operations.

Upgrade, downgrade to base, and re-upgrade were successfully exercised on a **separate disposable PostgreSQL database**, which was subsequently cleaned up. The persistent development database was not downgraded.

Future migrations must be reviewed before application. Backups and restore procedures are required before importing valuable real data. Do not run destructive downgrades on populated databases without explicit review.

## 7. Security and configuration

- Use ignored local `.env` configuration and a tracked placeholder `.env.example`; never commit credentials.
- Build connection URLs with SQLAlchemy `URL.create()` and avoid printing complete URLs.
- Restrict PostgreSQL host publication to localhost for Ubuntu development.
- Use parameterized SQLAlchemy queries and ensure sessions are closed.
- Keep migrations controlled and inspect generated operations before applying them.
- Review least-privilege database roles before production use; current local configuration does not establish production-grade privileges.
- Keep scanner reports and secrets outside Git; record evidence and findings in `docs/runbooks/security-findings.md`.
- Reassess SQLAlchemy, Psycopg, Alembic, and transitive dependencies when updating pins.

## 8. Testing and verification

Implemented verification includes:

| Area | Verification |
|---|---|
| Connectivity | Psycopg and SQLAlchemy `SELECT 1`; standalone `scripts/check_db_connection.py` |
| Sessions | `SessionLocal` and `get_db()` lifecycle checks |
| Schema | Tables, primary/foreign keys, checks, indexes and Alembic revision |
| Integrity | Invalid court count/latitude and orphan source rejected |
| ORM metadata | Declarative table, column, relationship and constraint tests |
| Migrations | Revision/structure tests and read-only PostgreSQL schema tests |
| Reversibility | Upgrade → downgrade → re-upgrade on disposable database |
| Regression | Existing FastAPI JSON API and Jinja2 tests remain passing |

Database integration tests are enabled locally with `RUN_DB_TESTS=1` and intentionally skip when not enabled, including CI environments without PostgreSQL. Skipped tests are not evidence of database connectivity. Repository search/filtering, API persistence integration, and import idempotency tests remain planned.

## 9. Deployment boundaries

Initial development uses PostgreSQL 17 in Docker Compose with a named persistent volume and localhost-only host port. The existing kind cluster and Terraform learning environment do not yet constitute a production database deployment. Containerized application connections use the Compose network host `db`, while Ubuntu-hosted Python uses the mapped localhost port. Production secret management, backups, access controls, and network architecture require separate review.

## 10. Exercise status

| Exercise | Status |
|---|---|
| 1 — Architecture and planning | Documented; updated to reflect implemented design |
| 2 — Connectivity and configuration | Implemented, tested, committed and pushed to feature branch |
| 3 — ORM models and Alembic | Implemented and verified locally; final security review and GitHub merge pending |
| 4 — Repository/service integration | Planned; current application still uses fictional records |
| 5 — Authorized public court import | Planned |
| 6 — Final review, merge and snapshot | Planned |

## 11. Related documentation

- `README.md`
- `docs/requirements/project-requirements.md`
- `docs/requirements/feature-backlog.md`
- `docs/architecture/system-overview.md`
- `docs/architecture/frontend-overview.md`
- `docs/security/security-policy.md`
- `docs/runbooks/security-findings.md`


## Phase 8 Exercise 4 — Consolidated Documentation Checkpoint (2026-11-18)

**Status:** Implementation in progress; final Exercise 4 regression, security, deployment review, commit and CI confirmation remain subject to verification. This checkpoint does not declare Phase 8 complete.

- PostgreSQL 17 runs locally through Docker Compose. SQLAlchemy 2.x, Psycopg 3, and Alembic are configured. The initial `courts` and `court_sources` schema is at Alembic revision `70a0a04f5a58`; upgrades, downgrades, and re-upgrades were verified against a disposable database.
- The application court service now uses `app/db/repositories/court_repository.py` and `app/api/mappers/court_mapper.py` to retrieve and map persistent records to the existing Pydantic `Court` response. FastAPI JSON and Jinja2 court routes use the `get_db` session dependency.
- Existing API paths, nested location fields, search and public filtering, HTTP 404/422 handling, and trusted Google Maps directions generation remain the intended compatibility contract.
- The `dc_tennis_test` database holds transaction-isolated fictional fixtures for tests. Existing three-court assumptions are being adapted to those fixtures. The latest reported full run was 80 passed, 2 failed, 1 warning; the two accessibility-test failures were traced to obsolete service signatures, and a subsequent syntax error was identified. A clean final full-suite result has not yet been supplied.
- The normal development database is not seeded with fictional fixtures; real public court records, verified operating hours and closure persistence, provenance-based import, and scheduling remain future work. Published hours must not be presented as guaranteed occupancy or official reservations.
- PostgreSQL integration tests are opt-in through `RUN_DB_TESTS=1`; CI without a PostgreSQL service skips database-dependent tests. A PostgreSQL-backed CI job remains planned. Container/Kubernetes database networking and production-readiness require separate validation.
- Security review continues to track `SEC-FE-001`, historical Trivy image findings, and the Phase 8 OpenTelemetry advisory `CVE-2026-126360`. Record a resolved status only with actual patched-dependency and rescan evidence; preserve all historical results.
- **Documentation cadence:** Routine documentation edits are deferred after this checkpoint until Phase 8 Exercise 6. Continue recording consequential security findings, architecture decisions, and migration changes when they occur. Before final merge, reconcile all eight canonical project documents against the actual repository and verified test/CI evidence.