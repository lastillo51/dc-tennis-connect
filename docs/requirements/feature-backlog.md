# DC Tennis Connect — Feature Backlog

## 1. Purpose

This document tracks implemented, planned, and future functionality for DC Tennis Connect.

The feature backlog supports incremental application development and ensures that new features can be introduced without unnecessarily disrupting existing components.

**Current Development Phase:** Phase 7 — Completed

**Next Development Phase:** Phase 8 — PostgreSQL application persistence and real public court data. Phase 7 frontend work has been squash-merged into `main`.

## 2. Feature Management Principles

- Develop features incrementally.
- Prioritize functionality based on user needs and project goals.
- Maintain modular and extensible application components.
- Update requirements and architecture documentation when functionality changes.
- Evaluate security, privacy, testing, accessibility, and cost implications.
- Use dedicated Git branches for development.
- Review changes through GitHub pull requests.
- Preserve existing functionality and API compatibility.
- Verify features before marking them completed.

### Feature Tracking

The backlog uses two types of identifiers:

| Identifier | Purpose |
|---|---|
| `FB-XXX` | Tracks application features across development phases |
| `FE-XXX` | Tracks implementation tasks specific to Phase 7 frontend development |

Feature identifiers shall remain stable.

Completing a Phase 7 task does not automatically mean its corresponding application feature is fully implemented.

## 3. Feature Priorities

### Must Have

- Responsive web application.
- Public tennis court directory.
- Court addresses and geographic locations.
- Published operating hours and known closures.
- Court scheduling classifications.
- Google Maps navigation.
- Public court information source attribution.

### Should Have

- Player registration and profiles.
- Tennis skill ratings.
- Player availability preferences.
- Hitting partner matching.
- Match invitations.
- Player match scheduling.
- Email and SMS notifications.

### Could Have

- In-app messaging.
- Court ratings and reviews.
- Social media integration.
- Interactive map displaying multiple courts.
- Distance-based court filtering.

### Future Enhancements

- Automated public court schedule updates.
- Enhanced player matching.
- Dedicated iOS and Android applications.
- Advanced monitoring and analytics.

## 4. Application Feature Backlog

This table tracks the overall application functionality.

| ID | Feature | Priority | Status | Planned Phase |
|---|---|---|---|---|
| FB-001 | Responsive web interface | Must Have | Completed — implemented and merged | Phase 7 |
| FB-002 | Public court directory | Must Have | Partially Implemented | Phases 2B, 7–8 |
| FB-003 | Court operating hours and closures | Must Have | Partially Implemented — sample hours displayed; verified data and closures pending | Phase 8 |
| FB-004 | Court availability classifications | Must Have | Partially Implemented — classifications displayed using sample data | Phase 8 |
| FB-005 | Google Maps navigation | Must Have | Completed — implemented and merged; SEC-FE-001 tracked | Phases 2B, 7 |
| FB-006 | Court data source attribution | Must Have | Planned | Phase 8 |
| FB-007 | Player profiles | Should Have | Planned | Phase 9 |
| FB-008 | Tennis skill ratings | Should Have | Planned | Phase 9 |
| FB-009 | Player availability preferences | Should Have | Planned | Phase 9 |
| FB-010 | Hitting partner matching | Should Have | Planned | Phase 9 |
| FB-011 | Match invitations and scheduling | Should Have | Planned | Phase 9 |
| FB-012 | Email notifications | Should Have | Planned | Future |
| FB-013 | SMS notifications | Should Have | Planned | Future |
| FB-014 | In-app messaging | Could Have | Backlog | Future |
| FB-015 | Court ratings and reviews | Could Have | Backlog | Future |
| FB-016 | Interactive court map | Could Have | Backlog | Future |
| FB-017 | Automated schedule synchronization | Future | Backlog | Future |
| FB-018 | Native mobile applications | Future | Backlog | Future |

### Implementation Notes

**FB-001 — Responsive Web Interface:** FastAPI/Jinja2 homepage, directory and detail pages, responsive CSS, and keyboard-navigation improvements have been implemented, tested, and merged into `main`.

**FB-002 — Public Court Directory:** Searchable, filterable court listings and detail pages work with three fictional sample records. Real Washington, D.C. public court data remains planned for Phase 8.

**FB-003 and FB-004 — Operating Hours and Availability:** The court schema and detail pages support operating hours and availability classifications, including missing information. Verified public hours, closure notices, and real availability data are not yet integrated. Published hours do not guarantee an unoccupied court.

**FB-005 — Google Maps Navigation:** Court detail pages generate directions through `app/api/services/maps_service.py` using a fixed Google Maps HTTPS endpoint and URL-encoded court location. The frontend behavior has been tested; the `SEC-FE-001` generic template-URL Semgrep finding remains under investigation and must be dispositioned under the security policy.

**FB-006 — Source Attribution:** Real public data sources and user-visible attribution remain planned. Fictional records are not represented as verified public court information.

## 5. Phase 7 — Frontend Development Backlog

Phase 7 focuses on creating a responsive web interface using FastAPI, Jinja2, HTML, CSS, and minimal JavaScript.

The frontend will reuse the existing court service layer and preserve current JSON API functionality.

### 5.1 Implementation Tasks

| ID | Feature | Priority | Status | Exercise |
|---|---|---|---|---|
| FE-001 | Frontend architecture and documentation | High | Completed — Exercise 1 merged | Exercise 1 |
| FE-002 | Jinja2 template integration | High | Completed — implemented and tested; merged into `main` | Exercise 2 |
| FE-003 | Frontend homepage | High | Completed — implemented and tested; merged into `main` | Exercise 2 |
| FE-004 | Court directory interface | High | Completed — sample records; merged into `main` | Exercise 3 |
| FE-005 | Court search and filtering | High | Completed — implemented and tested; merged into `main` | Exercise 3 |
| FE-006 | Individual court detail pages | High | Completed — implemented and tested; merged into `main` | Exercise 4 |
| FE-007 | Google Maps navigation | High | Completed — security finding tracked; merged into `main` | Exercise 4 |
| FE-008 | Responsive CSS layout | High | Completed — responsive checks performed; merged into `main` | Exercises 4–5 |
| FE-009 | Empty and error states | Medium | Partially Implemented — empty search and HTTP 404/422; styled error pages pending | Exercises 3–5 |
| FE-010 | Frontend accessibility review | High | Completed — initial review and regression checks; further WCAG audit remains future work | Exercise 5 |
| FE-011 | Automated frontend tests | High | Completed — regression suite implemented; final count to record; merged into `main` | Exercises 2–5 |
| FE-012 | Docker and Kubernetes compatibility verification | High | Completed — local checks reported; evidence to retain; merged into `main` | Exercise 5 |
| FE-013 | Final documentation and GitHub integration | High | Completed — Phase 7 pull request squash-merged; completion-status update follows | Exercises 5–6 |

**Status convention:** “Completed” here means the scoped frontend implementation was merged and verified, not that all future enhancements or security findings are resolved. FE-009 remains partial because styled error pages are not yet implemented. Preserve outstanding CI and deployment evidence in the security register.

### 5.2 Frontend Routing

The implemented frontend uses dedicated web routes without replacing existing JSON API endpoints.

| Route | Purpose |
|---|---|
| `/web` | Frontend homepage |
| `/web/courts` | Court directory |
| `/web/courts/{court_id}` | Court detail page |
| `/courts/` | Existing JSON court API |
| `/health` | Existing health endpoint |
| `/docs` | Existing Swagger UI |

The frontend currently uses fictional court records.

### 5.3 Phase 7 Acceptance Criteria

Phase 7 completion was assessed against these criteria:

1. The homepage renders successfully.
2. The court directory displays existing fictional court records.
3. Court search and filtering operate correctly.
4. Individual court detail pages display available information.
5. Google Maps navigation links function correctly.
6. Missing court records produce appropriate responses.
7. Empty search results display understandable messages.
8. The interface supports desktop and mobile viewport sizes.
9. Existing JSON API endpoints remain functional.
10. Automated frontend and backend tests pass.
11. Docker and Kubernetes deployments remain compatible.
12. Frontend changes complete applicable security checks, and blocking findings are remediated or formally dispositioned under policy.
13. Documentation is updated, the feature branch passes required CI checks, and changes are merged into `main`.

### 5.4 Deferred Features

The following features remain outside Phase 7:

- Authentication and player profiles.
- Player matching and scheduling.
- Real public court data ingestion.
- PostgreSQL application persistence.
- Automated court schedule synchronization.
- Public cloud deployment.

These features will be introduced in later phases.

## 6. Feature Status Definitions

| Status | Definition |
|---|---|
| Backlog | Proposed functionality not yet scheduled |
| Planned | Approved functionality awaiting implementation |
| In Progress | Functionality currently being developed |
| In Review | Implementation awaiting validation or pull-request review |
| Partially Implemented | Some supporting functionality exists, but the complete feature is unavailable |
| Completed | Functionality implemented, tested, and verified |
| Deferred | Functionality postponed to a later phase |
| Cancelled | Functionality no longer planned |

### Completion Requirements

A feature should only be marked **Completed** when:

- Its defined acceptance criteria are satisfied.
- Relevant automated tests pass.
- Applicable security checks are reviewed.
- Related documentation is updated.
- The implementation has been merged into `main`.

## 7. Adding New Features

When new functionality is requested:

1. Create a backlog entry with a unique identifier.
2. Define the feature's purpose and expected user benefit.
3. Identify the affected functional and nonfunctional requirements.
4. Evaluate dependencies and existing application components.
5. Assess security, privacy, accessibility, and cost implications.
6. Assign a priority and development phase.
7. Define measurable acceptance criteria.
8. Update architecture and requirements documentation as needed.
9. Implement the change on a dedicated Git branch.
10. Run automated tests and applicable security scans.
11. Review changes through a GitHub pull request.
12. Merge approved changes into `main`.
13. Update the backlog status after verification.

Feature identifiers shall not be reused when a feature is deferred or cancelled.

## 8. DevSecOps Considerations

Each feature shall be evaluated for applicable security and operational requirements.

### Application Security

- Input validation.
- Authentication and authorization where applicable.
- Safe handling of user-provided and external data.
- Protection of sensitive information.
- Secure external navigation links.

### Frontend Security

- Jinja2 template autoescaping.
- Validation of search and filtering parameters.
- Avoidance of unsafe HTML rendering.
- Controlled use of JavaScript and third-party assets.
- Appropriate browser security controls.

### Automated Verification

- Pytest regression tests.
- Semgrep static security analysis.
- Trivy container scanning.
- Terraform infrastructure validation where applicable.
- GitHub Actions CI checks.

### Deployment and Operations

- Docker compatibility.
- Kubernetes compatibility.
- Infrastructure configuration review.
- Logging and troubleshooting.
- Deployment and rollback considerations.

Security controls will expand as authentication, persistent user information, and public cloud deployment are introduced.

## 9. Development Phase Alignment

| Phase | Focus | Status |
|---|---|---|
| Phase 1 | Development environment | Complete |
| Phase 2A | Git, GitHub, and documentation | Complete |
| Phase 2B | FastAPI application foundation | Complete |
| Phase 3 | Docker and Docker Compose | Complete |
| Phase 4 | Security scanning and GitHub Actions | Complete |
| Phase 5 | Kubernetes with kind | Complete |
| Phase 6 | Terraform and Infrastructure as Code | Complete |
| Phase 7 | Responsive frontend development | Completed |
| Phase 8 | PostgreSQL integration and real court data | Planned |
| Phase 9 | Player accounts and match scheduling | Planned |
| Phase 10 | Cloud deployment and public HTTPS access | Planned |
| Phase 11 | Production security and operational readiness | Planned |

## 10. Backlog Maintenance

This document shall be reviewed when:

- New application requirements are introduced.
- Existing features are implemented or modified.
- Development phases change.
- Security or architecture decisions affect functionality.
- Features are deferred or cancelled.
- Pull requests implementing tracked features are merged.

### Maintenance Process

1. Review the current backlog.
2. Update feature statuses using verified implementation evidence.
3. Add new features without changing existing identifiers.
4. Update phase assignments when necessary.
5. Verify consistency with project requirements and architecture documentation.
6. Review changes through GitHub pull requests.

## 11. Current Project Status

**Current Phase:** Phase 7 — Completed  
**Next Phase:** Phase 8 — PostgreSQL application persistence and real public court data  
**Repository baseline:** Phase 7 frontend pull request squash-merged into `main`; local and remote `main` synchronized, and frontend feature branches removed.

### Completed Phase 7 Scope

- FastAPI/Jinja2 homepage, court directory, detail pages, search, public-only filtering, and Google Maps directions.
- Responsive styling and initial accessibility improvements, including automated frontend accessibility tests.
- Preservation of the existing JSON API and shared court services.
- Local Docker and kind Kubernetes frontend compatibility verification.
- Frontend and backend regression testing, security scanning, architecture updates, and GitHub integration.

### Outstanding Work and Evidence

- Real public court data, database persistence, player accounts, and match scheduling are future phases.
- Styled error pages and a broader WCAG audit remain follow-up improvements.
- `SEC-FE-001` remains tracked pending an evidence-supported disposition; Trivy High findings require triage.
- Final CI run identifiers and any incomplete scan metadata remain in `docs/runbooks/security-findings.md` until verified.

**Long-Term Goal:** Deliver a secure, publicly accessible application that helps Washington, D.C. tennis players discover courts, coordinate matches, and navigate to playing locations. Public production deployment is not yet approved.