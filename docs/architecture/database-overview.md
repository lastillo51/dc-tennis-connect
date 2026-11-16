# DC Tennis Connect — Database Architecture

**Current phase:** Phase 8 — Exercise 1 (planning)  
**Implementation status:** Proposed; not yet deployed as an application data store.

## 1. Purpose and boundaries

Introduce PostgreSQL-backed public tennis court information without breaking the Phase 7 FastAPI JSON API, Jinja2 pages, court service, or Google Maps directions. This phase does not implement player accounts, official court reservations, or real-time court occupancy.

## 2. Proposed technology

| Component | Proposed technology | Role |
|---|---|---|
| Persistence | PostgreSQL | Store verified court and source records |
| Data access | SQLAlchemy 2.x | Models, queries, repository boundary |
| Driver | Psycopg 3 | PostgreSQL connectivity |
| Schema migrations | Alembic | Versioned upgrade scripts |
| Tests | Pytest | Constraints, repository, migration, and API regressions |
| Local runtime | Existing Docker Compose | PostgreSQL service to inspect and reuse |

These packages are **not added to `requirements.txt` during Exercise 1**. Versions will be selected and tested in Exercises 2–3.

## 3. Data access flow

Browser → FastAPI web/API routes → shared court service → SQLAlchemy repository → PostgreSQL.

The service maps persistent records to the existing `Court` Pydantic schema. Templates never query the database. The existing Maps service derives fixed-host Google Maps URLs from validated locations.

## 4. Initial entities (proposed)

### `courts`

| Field | Type | Rule |
|---|---|---|
| `id` | INTEGER primary key | Positive identifier |
| `name` | VARCHAR(100) | Required, nonempty |
| `address` | VARCHAR(200) | Required, nonempty |
| `latitude` | DOUBLE PRECISION | Nullable; between -90 and 90 |
| `longitude` | DOUBLE PRECISION | Nullable; between -180 and 180 |
| `number_of_courts` | INTEGER | At least 1 |
| `public_access` | BOOLEAN | Required |
| `availability_status` | VARCHAR(40) | Controlled classification |
| `reservation_required` | BOOLEAN | Required; default false |
| `created_at`, `updated_at` | TIMESTAMPTZ | Required, UTC-aware |

### `court_sources`

| Field | Type | Rule |
|---|---|---|
| `id` | INTEGER primary key | Required |
| `court_id` | INTEGER foreign key | References `courts.id` |
| `publisher` | VARCHAR(150) | Required |
| `source_url` | TEXT | Validated permitted source URL when available |
| `source_identifier` | VARCHAR(200) | Optional stable upstream ID |
| `last_verified_at` | TIMESTAMPTZ | Required for imported real records |
| `source_type` | VARCHAR(50) | Controlled category |

Decide uniqueness keys and handling of multiple sources per court before the first migration. Operating hours, closures, and restrictions will be designed after inspecting actual authorized source formats. Preserve the existing optional `operating_hours` and `source_url` API fields during transition; unknown values remain null.

## 5. Data integrity and import

- Confirm authorized access and reuse before importing public data.
- Require provenance and verification time for each real record.
- Validate addresses, counts, coordinates, classifications, and dates.
- Identify duplicate court identities and make imports repeatable (idempotent).
- Keep fictional test fixtures separate from real court records.
- Clearly distinguish published operating hours from reservations and physical occupancy.
- Record errors and source changes without exposing credentials.

## 6. Migrations and rollback

Alembic migration files will be committed and reviewed. Verify schema upgrades in a disposable local database, plan backups before importing important data, and document recovery steps. Do not use destructive migration operations against populated databases without review.

## 7. Security and configuration

Use least-privilege database credentials supplied outside Git, restricted local networking, parameterized queries, and safe error messages. Do not store secrets in templates, logs, or scan reports committed to the repository. Reassess container and dependency vulnerabilities after adding packages.

## 8. Testing plan

Test connectivity, schema constraints, repository search/filtering, unknown court behavior, API compatibility, Jinja2 rendering, migration upgrades, and import validation/idempotency. Maintain existing Phase 7 regression tests.

## 9. Deployment boundaries

Initial development uses local PostgreSQL in Docker Compose. Local kind integration and future cloud-managed PostgreSQL require separate configuration and security reviews. Terraform currently provides a local learning foundation, not production database provisioning.

## 10. Exercise status

Exercise 1: planning and documentation only. Database connectivity, ORM models, migrations, and real court imports are not yet implemented.

## 11. Related documentation

- `README.md`
- `docs/requirements/project-requirements.md`
- `docs/requirements/feature-backlog.md`
- `docs/architecture/system-overview.md`
- `docs/architecture/frontend-overview.md`
- `docs/security/security-policy.md`
- `docs/runbooks/security-findings.md`