# DC Tennis Connect

**A Washington, D.C. tennis court discovery and player coordination platform — built as a hands-on DevSecOps learning project.**

**Current development phase:** Phase 9 — Exercise 1 (Real Court Data Readiness)  
**Previous phase:** Phase 8 — Completed and merged into `main` on November 25, 2026  
**Project status:** Active development on `feature/real-court-data`  
**Deployment status:** Local development and local kind Kubernetes; not approved for public deployment

> **Current-state summary (2026-11-25):** Phase 8 delivered PostgreSQL-backed court discovery and validated court-import infrastructure. Phase 9 begins with review and approval of real DPR facility data, followed by controlled import and the foundation for voluntary community scheduling. Historical checkpoints at the end of this README document earlier development states and do not supersede this summary.

## 1. Project Overview

DC Tennis Connect aims to help players discover public tennis courts in Washington, D.C., review published operating and reservation information, find hitting partners, coordinate matches, and obtain Google Maps directions.

The current frontend and JSON API read court records from PostgreSQL through SQLAlchemy. Fictional court records are used in isolated tests. Official DC GIS data has been evaluated as import candidates, but real DPR facilities have not yet been approved and imported into the development application. Player coordination and community scheduling are not implemented.

**Availability disclaimer:** DC Tennis Connect does not currently reserve public courts, report verified real-time occupancy, or guarantee that a court is physically unoccupied. Future community bookings will be voluntary arrangements, not official DPR reservations or exclusive rights to a court.

### Project Goals

- **Application:** Simplify tennis planning through court discovery, trustworthy published information, navigation, and future player coordination.
- **Learning:** Build practical DevSecOps skills across source control, testing, containers, security scanning, CI/CD, Kubernetes, and infrastructure as code.

## 2. Current Implementation

### Implemented and tested

- Python FastAPI backend, modular JSON API, and health endpoint.
- PostgreSQL 17 persistence, SQLAlchemy 2.x ORM and sessions, Psycopg 3 connectivity, and Alembic migrations.
- PostgreSQL-backed court service and Pydantic response schemas; fictional records remain in isolated test fixtures.
- Case-insensitive court-name and address search, public-access filtering, and validated query parameters.
- Server-rendered Jinja2 homepage, court directory, and individual court detail pages.
- Court details including address, number of courts, access classification, operating hours when available, and official reservation policy (`Unknown` when not verified).
- Google Maps directions generated from court locations through the existing Maps service, without a paid Maps API key.
- Responsive CSS, semantic HTML, keyboard navigation, and accessibility-oriented tests.
- DC GIS Layer 9 candidate validation, source-identity comparison, read-only import planner, and dry-run CLI.
- Explicit approval manifest and controlled test-database-only import command; rollback and duplicate-identity tests.
- Pytest backend, frontend, API, migration, and database integration coverage.
- Docker/Docker Compose development environment, including local PostgreSQL with persistent storage.
- Local Kubernetes deployment using kind, with a Deployment, ClusterIP Service, ConfigMap, health probes, resource limits, and container security contexts.
- Terraform local infrastructure-as-code foundation and CI validation.
- GitHub Actions workflows, Semgrep static analysis, and Trivy image/IaC scanning.

### Planned or incomplete

- Independent verification and approval of real DPR facilities, operating hours, and access information.
- Import and publication of approved real court records; persistent approval evidence and verification timestamps.
- Cross-source facility deduplication, controlled updates, and production-ready import authorization.
- Player registration, authentication, profiles, and skill ratings.
- Voluntary community court scheduling, conflict prevention, and player coordination.
- Hitting partner matching, invitations, and notifications.
- QR-code-based court adoption, real schedule synchronization, and native mobile applications.
- Public cloud deployment, HTTPS hosting, production monitoring, and security approval.

### Implementation status summary

| Component | Current status |
|---|---|
| FastAPI JSON API and court service | Implemented; PostgreSQL-backed |
| Jinja2 homepage, directory, and detail pages | Implemented |
| Search and public-only filtering | Implemented |
| Google Maps directions | Implemented using fixed-host URL generation |
| Responsive CSS and accessibility improvements | Implemented; ongoing review |
| PostgreSQL, SQLAlchemy, Psycopg, and Alembic | Implemented in Phase 8 |
| Court-source identity and nullable official reservation policy | Implemented in Phase 8 |
| DC GIS validation and read-only import planning | Implemented in Phase 8 |
| Approved real DPR data import | Pending Phase 9 verification and safeguards |
| Automated regression and database integration tests | Verified at Phase 8 completion; rerun per change |
| Docker and local kind deployment | Implemented for local development |
| Terraform local foundation | Phase 6 completed |
| Community scheduling foundation | Planned for Phase 9 |
| Player accounts and hitting-partner matching | Planned; scheduling depends on further design |
| Public cloud deployment | Planned — Phase 10 |

### Database verification and import commands

```bash
# From repository root, with a configured, ignored .env
python -m alembic current
python -m alembic check
python -m scripts.check_db_connection
DB_NAME=dc_tennis_test RUN_DB_TESTS=1 python -m pytest app/tests/ -q
RUN_DB_TESTS=0 python -m pytest app/tests/ -q
DB_NAME=dc_tennis_test python -m scripts.import_public_courts --dry-run
```

The latest Phase 8 Alembic revision is `61174a56cf41`. The dry-run CLI requires a locally saved `data/source-evaluation/dpr-tennis-candidates.json` and is restricted to disposable database names. `scripts/apply_public_courts.py` is **test-only**, requires `--apply --database dc_tennis_test`, and the checked-in approval manifest contains no approved real facilities. Confirm target database identity and backup requirements before any schema change or write operation. See [`docs/architecture/database-overview.md`](docs/architecture/database-overview.md) and [`docs/runbooks/repository-snapshot-management.md`](docs/runbooks/repository-snapshot-management.md).

## 3. Planned Application Features

### Must Have

- Responsive browser-based interface (foundation implemented).
- Public tennis court directory with names, addresses, and verified coordinates where available (interface implemented; real-data population pending).
- Published operating hours, known closures, restrictions, and reservation information from authorized sources.
- Clearly distinguished scheduling and availability classifications.
- Google Maps directions (implemented).
- Attribution and verification dates for real public court information.
- Voluntary community scheduling with clearly stated limitations (planned).

### Should Have

- Player registration, profiles, and tennis skill ratings.
- Player availability preferences and hitting-partner matching.
- Match invitations and scheduling.
- Email and SMS notifications.

### Could Have

- In-app messaging, social integration, court reviews, and interactive multi-court maps.

### Future Enhancements

- Authorized automated public schedule synchronization, proximity and distance filters, QR-code court adoption, and native mobile apps.

## 4. Current and Planned User Workflows

**Available now with records present in the configured database:**

1. Open the homepage and navigate to the court directory.
2. Search by court name or address, optionally filtering for public access.
3. Open a court detail page to review recorded information and availability classification.
4. Open Google Maps directions for the selected court.

The development database is not yet populated with the approved real DPR dataset; isolated test fixtures use fictional courts.

**Planned after real-data and scheduling features are added:**

1. Review attributed, published operating hours, restrictions, closures, and reservation information.
2. Select a court and potential playing time.
3. Create or join a voluntary community booking, subject to conflict checks.
4. Invite a hitting partner and coordinate a session.
5. View accepted sessions in player schedules.

A session scheduled through DC Tennis Connect will **not** constitute an official court reservation or guarantee court access.

## 5. Court Availability Approach

Court operating information will be drawn from reliable, authorized public sources, potentially including DC Department of Parks and Recreation, DC Open Data, official public reservation systems where reuse is permitted, and published facility schedules and closure notices.

The application distinguishes published hours, reservable facilities, first-come-first-served access, closures, and unknown availability. The initial real-data MVP will use manually verified information. Automated updates require source-permission and reliability review.

**Community scheduling is separate from official DPR reservations.** Proposed community time slots represent voluntary coordination among participating players; they do not convey exclusive use or report verified real-time occupancy. Unknown official reservation requirements remain `NULL` in PostgreSQL and display as `Unknown` in the frontend.

## 6. Technology Stack

| Category | Technology | Status |
|---|---|---|
| Version control | Git and GitHub | Implemented |
| Backend | Python and FastAPI | Implemented |
| Frontend | HTML, CSS, Jinja2 | Implemented; no JavaScript framework required currently |
| Database | PostgreSQL 17, SQLAlchemy 2.x, Psycopg 3, Alembic | Implemented for local application persistence |
| Containers | Docker Engine and Docker Compose | Implemented |
| Infrastructure as Code | Terraform | Local foundation implemented |
| Orchestration | Kubernetes and kind | Implemented locally |
| Container and IaC scanning | Trivy | Implemented; findings tracked |
| Static security analysis | Semgrep | Implemented; findings tracked |
| CI | GitHub Actions | Implemented |
| Testing | Pytest | Implemented; PostgreSQL integration tests opt-in |
| Navigation | Google Maps URLs | Implemented without a Maps API key |

## 7. Development Environment and Local Access

Primary environment: Ubuntu Desktop 26.04.1 LTS, VMware Workstation Pro, Visual Studio Code, Python virtual environments, Docker Engine/Compose, local kind Kubernetes, Git, and GitHub.

From the repository root, with PostgreSQL and required environment configuration available:

```bash
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000/web` | Homepage |
| `http://127.0.0.1:8000/web/courts` | Searchable directory |
| `http://127.0.0.1:8000/web/courts/{court_id}` | Detail page for an existing record |
| `http://127.0.0.1:8000/courts/` | JSON court API |
| `http://127.0.0.1:8000/health` | Health check |
| `http://127.0.0.1:8000/docs` | FastAPI interactive API docs |

Run tests with:

```bash
RUN_DB_TESTS=0 python -m pytest app/tests/ -q
DB_NAME=dc_tennis_test RUN_DB_TESTS=1 python -m pytest app/tests/ -q
python -m pip check
```

The frontend and JSON API share the same PostgreSQL-backed court service layer. The frontend generates Google Maps links through `app/api/services/maps_service.py`.

## 8. Project Structure

```text
dc-tennis-connect/
├── .github/workflows/
├── alembic/
│   └── versions/
├── app/
│   ├── api/
│   │   ├── mappers/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── session.py
│   ├── importers/
│   ├── web/routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── courts/
│   ├── static/css/styles.css
│   ├── tests/
│   └── main.py
├── scripts/
│   ├── import_public_courts.py
│   └── apply_public_courts.py
├── data/
│   └── import-approvals/
├── docker/
├── kubernetes/
├── terraform/
├── docs/
│   ├── requirements/
│   ├── architecture/
│   ├── security/
│   └── runbooks/
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

Locally downloaded GIS source data under `data/source-evaluation/` is not part of the committed repository snapshot.

## 9. DevSecOps Implementation and Security Status

- **Version control:** Dedicated feature branches, pull requests, and review before merging into `main`. Phase 8 was merged; Phase 9 work begins on `feature/real-court-data`.
- **Testing:** Automated backend, frontend, Maps, API, ORM, migration, and importer checks. Database-dependent tests use `RUN_DB_TESTS=1`; CI-style tests skip them without PostgreSQL.
- **Containers:** Non-root runtime configuration and local Docker verification.
- **Kubernetes:** Local kind deployment with probes, ConfigMap, resource limits, and security contexts.
- **Terraform:** Local infrastructure foundation, formatting/validation, and IaC scanning.
- **CI:** GitHub Actions checks for tests, dependencies, Semgrep, Trivy image scanning, and Terraform IaC. Phase 8 completion checks were reported passing; each future commit requires its own verification.
- **Frontend security:** Jinja2 escaping, FastAPI input validation, fixed-host Google Maps links, external-link protections, and regression tests.
- **Data import security:** Explicit approvals, stable source identifiers, source validation, restricted test-only writes, and rollback-isolated tests. Production import controls remain pending.

Security findings and decisions are tracked in [`docs/runbooks/security-findings.md`](docs/runbooks/security-findings.md). Historical findings, including `SEC-FE-001`, Trivy results, and OpenTelemetry advisory `CVE-2026-126360`, should retain their evidence-based dispositions. Historical counts are not a current vulnerability assessment. Successful scans do **not** mean the application is vulnerability-free.

The project remains **local-development only** and is **not approved for public production deployment**.

## 10. Development Roadmap

| Phase | Focus | Status |
|---|---|---|
| 1 | Development environment | Complete |
| 2A | Git, GitHub, and documentation | Complete |
| 2B | FastAPI foundation | Complete |
| 3 | Docker and Docker Compose | Complete |
| 4 | Security scanning and GitHub Actions | Complete |
| 5 | Kubernetes with kind | Complete |
| 6 | Terraform and infrastructure as code | Complete |
| 7 | Frontend implementation and hardening | Complete |
| 8 | PostgreSQL persistence and court-data import infrastructure | Complete — merged into `main` |
| 9 | Real court data import and community scheduling foundation | In Progress — Exercise 1 (readiness) |
| 10 | Public cloud deployment | Planned |
| 11 | Production security and operational readiness | Planned |

**Phase 8 completed work:** PostgreSQL connectivity, SQLAlchemy models and sessions, three Alembic migrations, database-backed court routes, source validation, dry-run planning, controlled test-only import infrastructure, and regression/security verification. Phase 8 was merged into `main` on November 25, 2026.

**Phase 9 initial plan:** Review DPR source evidence and facility identity, approve and safely import real facilities, validate published court data and Maps directions, design voluntary community scheduling, introduce scheduling models and migrations, and establish scheduling APIs with conflict prevention. Player accounts and hitting-partner matching remain planned work and may require further sequencing decisions.

## Historical Planning Record — Phase 8 Database and Public Court Data

> **Historical record, superseded by Phase 8 completion on November 25, 2026.** The following describes the original planning approach, not the current implementation status.

Phase 8 was planned to introduce persistent court records while preserving the existing FastAPI JSON contract, Jinja2 routes, and Google Maps directions. The proposed stack was PostgreSQL, SQLAlchemy 2.x, Psycopg 3, and Alembic. The initial design separated court identity and location from public source provenance, with no claim of real-time occupancy.

The planned sequence was to verify PostgreSQL Compose, establish secure connectivity, create models and reviewed migrations, introduce a repository layer, migrate API/frontend reads, and prepare authorized public-data imports while retaining fictional test fixtures. This infrastructure was implemented during Phase 8; publication of approved real DPR facilities remains Phase 9 work. See [`docs/architecture/database-overview.md`](docs/architecture/database-overview.md).

## 11. Cloud Deployment Goal

A later phase aims to provide a public HTTPS website usable from desktop and mobile browsers. Hosting decisions will consider cost, DNS, HTTPS, secure configuration, persistent data, automated deployment, logging, monitoring, backup/recovery, and security validation. Kubernetes and Terraform are options, not mandatory production hosting choices.

## 12. Security and Privacy

Development practices include least-privilege permissions, non-root containers, secret protection, input validation, Jinja2 escaping, trusted navigation URL generation, automated tests, scanning, and documented security reviews.

Relevant documents:

- [`docs/security/security-policy.md`](docs/security/security-policy.md)
- [`docs/runbooks/security-findings.md`](docs/runbooks/security-findings.md)

Real player data and authentication are not yet implemented. Public release requires additional security and privacy review.

## 13. Cost Considerations

The project prioritizes free and open-source technologies. Local development does not require paid cloud infrastructure, and Google Maps directions use standard URLs rather than a paid Maps API.

Potential later costs include cloud hosting, database storage, domains, SMS delivery, and third-party data services. Paid services must be evaluated and approved before use.

## 14. Documentation and Maintenance

Application requirements, architecture, feature backlog, security policies, scan findings, infrastructure configuration, and runbooks are maintained separately and version-controlled through GitHub.

Phase 8 was merged into `main` on November 25, 2026. Phase 9 development proceeds on `feature/real-court-data`. Routine documentation synchronization is planned for the end of Phase 9, with earlier updates when material architecture, security, or requirements decisions change.

For repository snapshot procedures, see [`docs/runbooks/repository-snapshot-management.md`](docs/runbooks/repository-snapshot-management.md).

## Historical Checkpoint — Phase 8 Exercise 4 (2026-11-18)

**Status:** Historical record — superseded by the completed Phase 8 implementation on November 25, 2026. The following bullets describe the state at that checkpoint, not the current application or test status.

- PostgreSQL 17 ran locally through Docker Compose. SQLAlchemy 2.x, Psycopg 3, and Alembic were configured. The initial `courts` and `court_sources` schema was at Alembic revision `70a0a04f5a58`; upgrades, downgrades, and re-upgrades were verified against a disposable database.
- The application court service used `app/db/repositories/court_repository.py` and `app/api/mappers/court_mapper.py` to retrieve and map persistent records to the existing Pydantic `Court` response. FastAPI JSON and Jinja2 court routes used the `get_db` session dependency.
- Existing API paths, nested location fields, search and public filtering, HTTP 404/422 handling, and trusted Google Maps directions generation remained the intended compatibility contract.
- The `dc_tennis_test` database held transaction-isolated fictional fixtures. At this checkpoint, the latest reported full run was 80 passed, 2 failed, 1 warning; the accessibility-test failures were traced to obsolete service signatures, and a subsequent syntax error was identified. These were later resolved during Phase 8.
- The development database was not seeded with fictional fixtures; real public court records, verified operating hours, closure persistence, provenance-based import, and scheduling remained future work. Published hours were not to be presented as guaranteed occupancy or official reservations.
- PostgreSQL integration tests were opt-in through `RUN_DB_TESTS=1`; CI without a PostgreSQL service skipped database-dependent tests. A PostgreSQL-backed CI job remained planned. Container/Kubernetes database networking and production-readiness required separate validation.
- Security review tracked `SEC-FE-001`, historical Trivy image findings, and OpenTelemetry advisory `CVE-2026-126360`. Resolved status required patched-dependency and rescan evidence.
- **Documentation cadence at that time:** Routine documentation edits were deferred until Phase 8 Exercise 6, when the canonical project documents would be reconciled against verified repository and CI evidence. That reconciliation was subsequently completed as part of the Phase 8 closeout.