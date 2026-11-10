# DC Tennis Connect

**A Washington, D.C. tennis court discovery and player coordination platform — built as a hands-on DevSecOps learning project.**

**Current development phase:** Phase 7 — Completed  
**Next development phase:** Phase 8 — PostgreSQL application persistence and real public court data  
**Project status:** Active development; Phase 7 merged into `main`  
**Deployment status:** Local development and local kind Kubernetes; not approved for public deployment

## 1. Project Overview

DC Tennis Connect aims to help players discover public tennis courts in Washington, D.C., review published operating and reservation information, find hitting partners, coordinate matches, and obtain Google Maps directions.

The **current application uses three fictional court records** for development and testing. Its frontend and JSON API are functional, but real public court data, player coordination, and official scheduling integrations have not yet been implemented.

**Availability disclaimer:** DC Tennis Connect does not reserve public courts, report verified real-time occupancy, or guarantee that a court is physically unoccupied.

### Project Goals

- **Application:** Simplify tennis planning through court discovery, trustworthy published information, navigation, and future player coordination.
- **Learning:** Build practical DevSecOps skills across source control, testing, containers, security scanning, CI/CD, Kubernetes, and infrastructure as code.

## 2. Current Implementation

### Implemented and tested

- Python FastAPI backend, modular JSON API, and health endpoint.
- In-memory fictional court dataset with a shared service layer and Pydantic models.
- Case-insensitive court-name and address search, public-access filtering, and validated query parameters.
- Server-rendered Jinja2 homepage, court directory, and individual court detail pages.
- Court details including address, number of courts, access classification, reservation requirement, and operating hours when present.
- Google Maps directions generated from court locations through the existing Maps service, without a paid Maps API key.
- Responsive CSS, semantic HTML, keyboard navigation, and accessibility-oriented tests and improvements.
- Pytest backend, frontend, API, and Maps-service regression coverage.
- Docker/Docker Compose development environment, including a local PostgreSQL container with persistent storage.
- Local Kubernetes deployment using kind, with a Deployment, ClusterIP Service, ConfigMap, health probes, resource limits, and container security contexts.
- Terraform local infrastructure-as-code foundation and CI validation.
- GitHub Actions workflows, Semgrep static analysis, and Trivy image/IaC scanning.

### Planned or incomplete

- Real, authorized Washington, D.C. public court data and source attribution.
- PostgreSQL persistence for application court and player records (a local PostgreSQL container exists, but application persistence is not integrated).
- Player registration, authentication, profiles, and skill ratings.
- Hitting partner matching, invitations, and match scheduling.
- Email/SMS notifications, real court schedule synchronization, and native mobile applications.
- Public cloud deployment, HTTPS hosting, production monitoring, and production security approval.

### Implementation status summary

| Component | Current status |
|---|---|
| FastAPI JSON API and court service | Implemented |
| Fictional court data and validation | Implemented |
| Jinja2 homepage, directory, and detail pages | Implemented on Phase 7 feature branch |
| Search and public-only filtering | Implemented |
| Google Maps directions | Implemented using existing URL-generation service |
| Responsive CSS and basic accessibility improvements | Implemented; continued review in Phase 7 |
| Automated regression tests | Passing at reported checkpoints; rerun before merge |
| Docker and local kind deployment | Implemented; frontend compatibility verified during Phase 7 exercises |
| Terraform local foundation | Phase 6 completed |
| Real public court data and application persistence | Planned — Phase 8 |
| Player accounts, matching, and scheduling | Planned — Phase 9 |
| Public cloud deployment | Planned — Phase 10 |

## 3. Planned Application Features

### Must Have

- Responsive browser-based interface (frontend foundation implemented).
- Public tennis court directory with names, addresses, and verified coordinates where available (fictional-data interface implemented).
- Published operating hours, known closures, restrictions, and reservation information from authorized sources.
- Clearly distinguished scheduling and availability classifications.
- Google Maps directions (implemented for sample courts).
- Attribution and verification dates for real public court information.

### Should Have

- Player registration, profiles, and tennis skill ratings.
- Player availability preferences and hitting partner matching.
- Match invitations and scheduling.
- Email and SMS notifications.

### Could Have

- In-app messaging, social integration, court reviews, and interactive multi-court maps.

### Future Enhancements

- Authorized automated public schedule synchronization, proximity and distance filters, and native mobile apps.

## 4. Current and Planned User Workflows

**Available now with fictional data:**

1. Open the homepage and navigate to the court directory.
2. Search by court name or address, optionally filtering for public access.
3. Open a court detail page to review recorded information and availability classification.
4. Open Google Maps directions for the selected court.

**Planned after real-data and player features are added:**

1. Review attributed, published operating hours, restrictions, closures, and reservation information.
2. Select a potential court and playing time.
3. Invite a compatible hitting partner and coordinate a session.
4. View accepted sessions in player schedules.

A proposed session in DC Tennis Connect will **not** constitute an official court reservation.

## 5. Court Availability Approach

Future court scheduling information will come from reliable, authorized public sources, potentially including DC Department of Parks and Recreation, DC Open Data, official public reservation systems where reuse is permitted, and published facility schedules and closure notices.

The application will distinguish published hours, reservable slots, published reservations, first-come-first-served access, closures, and unknown availability. The initial real-data MVP will use manually verified information. Automated updates require source-permission and reliability review.

The current sample records demonstrate the data model and UI; **they do not represent verified real court availability**.

## 6. Technology Stack

| Category | Technology | Status |
|---|---|---|
| Version control | Git and GitHub | Implemented |
| Backend | Python and FastAPI | Implemented |
| Frontend | HTML, CSS, Jinja2 | Implemented; no JavaScript framework required currently |
| Database | PostgreSQL | Local container configured; application persistence planned |
| Containers | Docker Engine and Docker Compose | Implemented |
| Infrastructure as Code | Terraform | Local foundation implemented |
| Orchestration | Kubernetes and kind | Implemented locally |
| Container and IaC scanning | Trivy | Implemented; findings under review |
| Static security analysis | Semgrep | Implemented; `SEC-FE-001` tracked |
| CI | GitHub Actions | Implemented |
| Testing | Pytest | Implemented |
| Navigation | Google Maps URLs | Implemented without a Maps API key |

## 7. Development Environment and Local Access

Primary environment: Ubuntu Desktop 26.04.1 LTS, VMware Workstation Pro, Visual Studio Code, Python virtual environments, Docker Engine/Compose, local kind Kubernetes, Git, and GitHub.

From the repository root:

```bash
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

| URL | Purpose |
|---|---|
| `http://127.0.0.1:8000/web` | Homepage |
| `http://127.0.0.1:8000/web/courts` | Searchable directory |
| `http://127.0.0.1:8000/web/courts/1` | Example detail page; use an existing sample court ID |
| `http://127.0.0.1:8000/courts/` | JSON court API |
| `http://127.0.0.1:8000/health` | Health check |
| `http://127.0.0.1:8000/docs` | FastAPI interactive API docs |

Run tests with:

```bash
python -m pytest app/tests/ -q
python -m pip check
```

The frontend and JSON API share the same court service layer. The frontend generates Google Maps links through `app/api/services/maps_service.py`.

## 8. Project Structure

```text
dc-tennis-connect/
├── .github/workflows/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   ├── web/routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── courts/
│   │       ├── index.html
│   │       └── detail.html
│   ├── static/css/styles.css
│   ├── tests/
│   └── main.py
├── docker/
├── kubernetes/
├── terraform/
│   ├── environments/
│   └── modules/
├── docs/
│   ├── architecture/
│   ├── security/
│   └── runbooks/
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## 9. DevSecOps Implementation and Security Status

- **Version control:** Dedicated feature branches, pull requests, and review before merging into `main`.
- **Testing:** Automated backend, frontend, Maps, and API checks. A previous Phase 7 checkpoint reported 42 passing tests; later additions require a fresh final count before merge.
- **Containers:** Non-root runtime configuration and local Docker verification.
- **Kubernetes:** Local kind deployment with probes, ConfigMap, resource limits, and security contexts.
- **Terraform:** Local infrastructure foundation, formatting/validation, and IaC scanning.
- **CI:** GitHub Actions checks for tests, dependencies, Semgrep, Trivy image scanning, and Terraform IaC. Actual run outcomes must be checked per commit.
- **Frontend security:** Jinja2 escaping, FastAPI input validation, generated fixed-domain Google Maps links, external-link protections, and regression tests.

Security findings and decisions are tracked in [`docs/runbooks/security-findings.md`](docs/runbooks/security-findings.md). The Semgrep template-link finding `SEC-FE-001` requires an evidence-based disposition. The Phase 7 Trivy image scan recorded 189 vulnerability findings (49 High, 75 Medium, 65 Low, 0 Critical, 0 Unknown) before subsequent evidence verification; use the latest recorded scan and review findings before any deployment decision. Successful scans do **not** mean the application is vulnerability-free.

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
| 7 | Frontend implementation and hardening | Completed |
| 8 | PostgreSQL application persistence and real court data | Planned |
| 9 | Player accounts, matching, and scheduling | Planned |
| 10 | Public cloud deployment | Planned |
| 11 | Production security and operational readiness | Planned |

**Phase 7 completed work:** frontend planning, homepage, directory, search/filtering, court detail pages, Maps navigation, accessibility improvements, security reviews, and local deployment checks. The Phase 7 pull request was squash-merged into `main`, and the feature branches were removed. The project remains in local development; outstanding security findings are tracked separately.

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

Update documentation when implementation or security decisions change. Phase 7 changes are merged into `main`. Begin Phase 8 work on a new feature branch after reviewing the requirements and security backlog.