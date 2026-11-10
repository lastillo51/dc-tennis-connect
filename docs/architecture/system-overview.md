# DC Tennis Connect — System Architecture

> **Current stage:** Phase 7 — Completed; frontend merged into `main`  
> **Next stage:** Phase 8 — PostgreSQL application persistence and real public court data  
> **Deployment scope:** Local development and testing; not approved for public production deployment.  
> **Document purpose:** Describe implemented architecture, planned components, and the boundaries between them.

## 1. Architecture Overview

DC Tennis Connect is a FastAPI application for helping Washington, D.C. tennis players discover courts and, in future phases, coordinate matches. The current application combines a JSON API with server-rendered Jinja2 pages. Both interfaces use shared Pydantic court models and service functions backed by **fictional in-memory sample records**.

Docker and Docker Compose support local container development. A local Kubernetes cluster created with kind provides an orchestration test environment. Terraform supports infrastructure-as-code learning through local resources and reusable modules. PostgreSQL is available in the local container environment but **application court and player records are not yet persisted there**.

The application does not reserve public courts or guarantee that a court is unoccupied. Public cloud hosting, verified DC court data, player accounts, and scheduling are not implemented.

### 1.1 Implemented request flow

```text
Browser
  |-- /web, /web/courts, /web/courts/{court_id}
  v
FastAPI frontend router (app/web/routes.py)
  |-- Jinja2 templates (app/templates/)
  |-- Static CSS (app/static/css/)
  |-- Court service (app/api/services/court_service.py)
  `-- Google Maps service (app/api/services/maps_service.py)

JSON API (/courts/) --> Shared court service --> Fictional sample records
Health endpoint (/health) --> FastAPI

Docker image --> Local Docker runtime / kind Kubernetes Deployment
Terraform --> Separate local infrastructure exercises
```

The frontend calls shared Python services directly; it does not make HTTP requests to its own JSON API.

## 2. Core Components and Responsibilities

| Component | Implementation | Current status |
|---|---|---|
| Backend and JSON API | Python, FastAPI, Pydantic | Implemented |
| Frontend | FastAPI web routes, Jinja2, HTML, CSS | Implemented with fictional data |
| Court retrieval and search | `app/api/services/court_service.py` | Implemented |
| Google Maps directions | `app/api/services/maps_service.py` | Implemented |
| Application records | In-memory fictional court dataset | Development-only |
| PostgreSQL | Local container with persistent storage | Configured; application persistence planned |
| Docker | Application image and Compose configuration | Implemented locally |
| Kubernetes | kind cluster, Deployment, Service, ConfigMap, probes, security context | Implemented locally |
| Terraform | Local environments, modules, validation and IaC scans | Foundation completed |
| CI and security | GitHub Actions, Pytest, Semgrep, Trivy | Implemented; findings require review |
| Player accounts and match scheduling | Planned services and persistent records | Not implemented |
| Public cloud deployment | Future HTTPS-hosted application | Not implemented |

### 2.1 Frontend structure

```text
app/
├── main.py
├── api/
│   ├── routes/
│   ├── schemas/
│   └── services/
│       ├── court_service.py
│       └── maps_service.py
├── web/
│   ├── __init__.py
│   └── routes.py
├── templates/
│   ├── base.html
│   ├── home.html
│   └── courts/
│       ├── index.html
│       └── detail.html
├── static/
│   └── css/
│       └── styles.css
└── tests/
```

This tree highlights relevant files, not every repository file. Custom HTML error templates and a JavaScript bundle are **not assumed to exist**; add them only when implemented.

### 2.2 Current routes

| Route | Response | Responsibility |
|---|---|---|
| `/web` | HTML | Homepage |
| `/web/courts` | HTML | Court directory, search, public-access filtering |
| `/web/courts/{court_id}` | HTML | Individual court details and directions |
| `/courts/` | JSON | Existing court API |
| `/health` | JSON | Health check |
| `/docs` | HTML | FastAPI API documentation |
| `/static/css/styles.css` | CSS | Local frontend stylesheet |

Unknown court IDs return HTTP 404; invalid typed parameters return HTTP 422. Custom styled error pages are a separate enhancement.

### 2.3 Frontend behavior and boundaries

The current interface displays court names, nested addresses, public-access information, court counts, availability classifications, and operating hours when present. It supports case-insensitive court name/address search and public-only filtering. Responsive layouts, keyboard navigation, semantic markup, and accessibility checks are part of Phase 7 hardening.

The frontend does **not** provide live occupancy, official reservations, real court data ingestion, authentication, persistent schedules, or player matching. A displayed availability classification is not evidence of real-time court availability.

## 3. Court Data and Availability Architecture

### 3.1 Current data model

Court records are represented by Pydantic models, including nested `CourtLocation` (address and optional coordinates), optional operating hours, public-access status, reservation-required flag, availability classification, and optional source metadata. The current records are fictional and held in memory.

### 3.2 Planned public data sources

Authorized sources may include:

- DC Department of Parks and Recreation.
- DC Open Data.
- Official public reservation systems where access and reuse are permitted.
- Published facility schedules and closure notices.

Each source must be checked for accuracy, permitted use, and update frequency before integration. The initial real-data implementation is expected to use manually verified public information; automation is conditional on source permissions.

### 3.3 Planned validation and freshness

Future persisted court records should distinguish published operating hours, reservable slots, published reservations, first-come-first-served access, known closures, and unknown availability. Where available, record source attribution, verification timestamps, and date-specific restrictions. Do not represent stale or unverified information as confirmed availability.

## 4. Google Maps Navigation

The detail-page route obtains a `CourtLocation` from the shared court service and calls `build_google_maps_url(court.location)`. The Maps service constructs a Google Maps directions URL using a fixed HTTPS endpoint and an encoded destination. Coordinates may be used when available; otherwise the address is used.

The rendered link opens Google Maps externally with `target="_blank"` and `rel="noopener noreferrer"`. The application does not calculate routes, collect the user's precise location, or require a paid Google Maps API key for these standard URLs.

**Security constraint:** Do not substitute arbitrary user-controlled URLs or the optional `court.google_maps_url` field as a direct link without appropriate validation. The dynamic Jinja2 `href` is tracked as Semgrep finding `SEC-FE-001`; its documented disposition and CI treatment remain subject to verification in `docs/runbooks/security-findings.md`.

## 5. Planned Player Matching and Scheduling

Future authenticated players will be able to select a court and proposed date/time, invite another player, accept or decline invitations, and view accepted sessions. Proposed match states include **Pending, Accepted, Declined, and Cancelled**.

Scheduling validation should reject past sessions, times outside verified operating hours, and verified closures; identify overlapping accepted matches and known conflicts; and warn when availability is unknown. A scheduled match represents an agreement between players, **not an official court reservation**. First-come-first-served courts may still be occupied upon arrival.

Planned PostgreSQL records include courts, locations, hours, closures, public sources, verification timestamps, player profiles, availability preferences, invitations, and matches. Public court schedules and player-created matches must remain logically separate: accepting a match must not change official reservation availability.

## 6. Local Development and Deployment

### 6.1 Development environment

- Ubuntu Desktop 26.04.1 LTS in VMware Workstation Pro.
- Git, GitHub, Visual Studio Code, Python virtual environment and `requirements.txt`.
- Docker Engine, Docker Compose, local PostgreSQL, kind, kubectl, and Terraform.

### 6.2 Docker

The application image packages FastAPI code, Jinja2 templates, and static CSS. Local verification should cover HTML, JSON API, health endpoint, CSS, and non-root runtime execution. Docker Compose provides local application/database services. Images require Trivy review; a successful scan does not mean all reported vulnerabilities are remediated.

### 6.3 Kubernetes

The local kind environment includes a Deployment, ClusterIP Service, ConfigMap, readiness/liveness probes, resource limits, and a restricted security context. Frontend image tests must verify HTML, CSS, and JSON endpoints after rollout. Changes made with `kubectl set image` affect the live cluster only; reconcile or restore Git-managed manifests so deployment configuration remains reproducible.

### 6.4 Terraform

Phase 6 established local Terraform resources, modules, variables, outputs, state handling, validation, and IaC scanning. It does **not** provision the public cloud application. Future cloud environments require decisions about state security, credentials, network exposure, and cost.

## 7. DevSecOps and Security Architecture

| Control | Current implementation / expectation |
|---|---|
| Source control | Feature branches, reviewed pull requests, synchronized `main` |
| Testing | Pytest for API, frontend, service and security regression behavior |
| Dependency checks | `python -m pip check` |
| Static analysis | Semgrep `p/security-audit` and documented finding disposition |
| Container scanning | Trivy vulnerability and secret-scanning evidence |
| IaC validation | Terraform formatting, validation, Trivy config scanning |
| CI | GitHub Actions for applicable branches and pull requests |
| Container security | Non-root execution and Kubernetes security contexts |
| Frontend security | Jinja2 autoescaping, input validation, trusted external URLs, controlled static assets |
| Accessibility | Semantic HTML, labeled controls, keyboard access, visible focus, responsive layouts |

Frontend browser security headers and Content Security Policy require compatibility review before enforcement. Do not enable HSTS on the local HTTP environment. Authentication, authorization, CSRF defenses for state-changing forms, production secrets, monitoring, and data protection are required as relevant functionality is introduced.

The application is **not approved for public deployment**. The security findings register tracks the Phase 7 `SEC-FE-001` investigation and Trivy frontend-image findings, including the recorded High-severity vulnerabilities. Do not interpret scanner execution or passing tests as risk acceptance.

## 8. Development Dependency Compatibility

Python dependencies are managed in `.venv` and the version-controlled `requirements.txt`. The following versions were recorded during the Phase 2B environment verification; they are **historical**, not a claim about currently installed versions.

| Dependency | Phase 2B recorded version |
|---|---|
| Python | 3.14 |
| FastAPI | 0.159.1 |
| Starlette | 1.9.0 |
| HTTPX | 0.28.1 |
| Pytest | 9.1.1 |

A known testing warning was reported:

```text
StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead.
```

The previously recorded regression baseline was **42 passed, 1 warning**. `python -m pip check` also passed at that checkpoint. Later test counts and package versions must be recorded from actual executions. This warning is a dependency-maintenance issue, not by itself a confirmed vulnerability.

**Decision:** Keep the working dependency set until official migration guidance and a compatible replacement have been evaluated. Do not upgrade or suppress the warning solely to make output quieter. Any migration should be tested in the virtual environment, followed by the full Pytest suite, `pip check`, security scans as applicable, and a reviewed `requirements.txt` update.

## 9. Future Cloud and Production Architecture

Before public access, design and verify:

- Authorized real court data ingestion, source attribution, and freshness controls.
- PostgreSQL application persistence and backups.
- Authentication, authorization, sessions, and privacy protections.
- HTTPS, DNS, network exposure, secret management, and secure browser headers.
- Monitoring, logging, recovery, and deployment/rollback workflows.
- Security findings remediation or formally reviewed risk decisions.
- Cost-aware hosting; managed Kubernetes is optional, not a requirement.

Public deployment should be gated on verified operational and security readiness, not merely successful local Kubernetes tests.

## 10. Architecture Status and Maintenance

| Area | Status |
|---|---|
| Phases 1–6 local DevSecOps foundations | Completed |
| Phase 7 frontend pages, court search, details, Maps navigation | Implemented, verified, and merged into `main` |
| Phase 7 accessibility, security and deployment hardening | Local implementation and verification completed; outstanding Semgrep/Trivy findings remain tracked |
| Phase 8 real court data and PostgreSQL persistence | Planned |
| Phase 9 player accounts and scheduling | Planned |
| Phase 10 cloud deployment | Planned |
| Phase 11 production security and operations | Planned |

Update this document when an implemented route, component, data source, deployment mechanism, or security boundary changes. Keep historical verification evidence in the relevant runbooks and do not silently replace planned capabilities with claims of implementation.

## 11. Related Documentation

- `README.md` — project overview, local usage, and roadmap.
- `docs/architecture/frontend-overview.md` — detailed frontend architecture.
- `docs/architecture/kubernetes-overview.md` — local Kubernetes architecture.
- `docs/architecture/terraform-overview.md` — Terraform foundation.
- `docs/requirements/feature-backlog.md` — implementation and future feature status.
- `docs/security/security-policy.md` — security requirements.
- `docs/runbooks/security-findings.md` — scan baselines, findings, and decisions.
- `.github/workflows/security-ci.yml` — CI implementation.