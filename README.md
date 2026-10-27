# DC Tennis Connect

**A Washington, D.C. tennis court discovery and player coordination platform — built as a hands-on DevSecOps learning project.**

**Current Development Phase:** Phase 6 — Terraform and Infrastructure as Code

**Project Status:** Active Development

## 1. Project Overview

DC Tennis Connect is a web-based application designed to help tennis players in Washington, D.C. discover public tennis courts, review published court scheduling information, coordinate hitting sessions, and obtain directions using Google Maps.

The application will use reliable, publicly available court information to help players identify potential playing times.

Players will eventually be able to organize matches around published operating hours, reservation information, and known court restrictions.

**Important:** DC Tennis Connect does not independently reserve public courts or guarantee that a court is physically unoccupied.

### Project Goals

**Application Goal**

Simplify tennis planning by combining public court discovery, published scheduling information, player matching, match coordination, and navigation.

**Learning Goal**

Gain practical experience implementing DevSecOps technologies throughout the software development lifecycle, including containerization, security scanning, CI/CD, Kubernetes, and infrastructure automation.

## 2. Current Implementation

The project currently provides a working FastAPI backend and a local DevSecOps development environment.

### Implemented

- Python FastAPI backend with modular API routing.
- Sample tennis court directory using fictional court records.
- Court filtering and request validation.
- Google Maps destination URL generation.
- Health-check endpoint.
- Automated application tests using Pytest.
- Docker containerization and Docker Compose configuration.
- Local PostgreSQL container with persistent storage.
- Trivy container vulnerability scanning.
- Semgrep static application security scanning.
- GitHub Actions CI workflow for testing and security checks.
- Local Kubernetes deployment using kind.
- Kubernetes Deployment and ClusterIP Service.
- Kubernetes ConfigMap integration.
- Kubernetes health probes, resource constraints, and security contexts.
- Git feature branching and pull request workflows.

### Not Yet Implemented

- Responsive end-user web interface.
- Real Washington, D.C. public tennis court data integration.
- Database persistence for application records.
- Player registration and authentication.
- Player profiles and skill ratings.
- Hitting partner matching.
- Match scheduling and invitations.
- Email and SMS notifications.
- Public cloud hosting and HTTPS access.

The current API uses fictional sample data for development and testing.

## 3. Planned Application Features

### Must Have

- Responsive web application accessible from desktop and mobile browsers.
- Public tennis court directory.
- Court names, addresses, and verified geographic coordinates where available.
- Published court operating hours.
- Publicly documented reservations, closures, and restrictions where available.
- Clearly identified court scheduling information.
- Google Maps directions.
- Source attribution for public court information.

### Should Have

- Player registration and profiles.
- Tennis skill ratings.
- Player availability preferences.
- Hitting partner matching.
- Match invitations and scheduling.
- Email and SMS notifications.

### Could Have

- In-app messaging.
- Social media integration.
- Court ratings and reviews.
- Interactive maps displaying multiple courts.

### Future Enhancements

- Automated public schedule synchronization.
- Location-based court search.
- Distance-based court filtering.
- Dedicated iOS and Android applications.

## 4. How the Application Will Work

The planned user workflow is:

1. A player searches for a public tennis court.
2. The application displays its location, published operating hours, reservation information, and known restrictions.
3. The player reviews potential playing times.
4. The player selects a court, date, and time for a proposed hitting session.
5. The player invites a compatible hitting partner.
6. The invited player accepts or declines.
7. Accepted matches appear in both players' schedules.
8. Players use Google Maps to navigate to the selected court.

Scheduling a match through DC Tennis Connect does not constitute an official court reservation.

Published operating hours do not guarantee that a court is physically unoccupied.

## 5. Court Availability Approach

Court scheduling information will come from reliable, authorized public sources.

Potential sources include:

- DC Department of Parks and Recreation.
- DC Open Data.
- Official court reservation platforms where information is publicly accessible and reuse is permitted.
- Published facility operating schedules and closure notices.

The application will distinguish between:

- Published operating hours.
- Verified reservable time slots.
- Published reservations.
- First-come, first-served access.
- Known closures.
- Unknown availability.

The initial MVP will use manually verified public information.

Automated updates may be introduced after confirming that the relevant sources permit programmatic access.

The application will not represent unverified availability as confirmed.

## 6. Technology Stack

| Category | Technology | Status |
|---|---|---|
| Version Control | Git and GitHub | Implemented |
| Backend | Python and FastAPI | Implemented |
| Frontend | HTML, CSS, JavaScript, Jinja2 | Planned |
| Database | PostgreSQL | Local container configured |
| Containers | Docker Engine and Docker Compose | Implemented |
| Infrastructure as Code | Terraform | Phase 6 — In Progress |
| Container Orchestration | Kubernetes and kind | Implemented locally |
| Container Security | Trivy | Implemented |
| Static Security Analysis | Semgrep | Implemented |
| CI/CD | GitHub Actions | Implemented |
| Testing | Pytest | Implemented |
| Navigation | Google Maps URLs | Backend URL generation implemented |

Technologies will be added or updated as the architecture evolves.

## 7. Development Environment

The primary development environment consists of:

- Ubuntu Desktop 26.04.1 LTS.
- VMware Workstation Pro.
- Visual Studio Code.
- Python virtual environments.
- Docker Engine and Docker Compose.
- Local kind Kubernetes cluster.
- Git and GitHub.

Development is currently performed locally before deployment to external infrastructure.

## 8. Project Structure

The repository is organized around application development, infrastructure, testing, and documentation.

```text
dc-tennis-connect/
├── .github/
│   └── workflows/
├── app/
│   ├── api/
│   └── tests/
├── docker/
│   ├── Dockerfile
│   └── compose.yaml
├── kubernetes/
│   ├── kind/
│   ├── base/
│   └── overlays/
├── terraform/
│   ├── environments/
│   │   ├── local/
│   │   └── cloud/
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

The Terraform directories are being introduced during Phase 6 and may initially be empty.

The structure is designed to support future application functionality and cloud environments without requiring a major reorganization.

## 9. DevSecOps Implementation

### Version Control

Git and GitHub are used for source control, feature branching, pull requests, and code review.

### Automated Testing

Pytest provides automated verification of the FastAPI application.

The current test suite contains 16 passing tests.

### Containerization

Docker packages the FastAPI application into a portable container.

Docker Compose provides the local application and PostgreSQL environment.

### Security Scanning

Trivy scans container images for known vulnerabilities.

Semgrep performs static analysis of application source code.

Security findings, remediation decisions, and outstanding risks are documented in `docs/runbooks/security-findings.md`.

### CI/CD

GitHub Actions automatically runs:

- Python application tests.
- Dependency consistency checks.
- Semgrep static security analysis.
- Trivy container vulnerability scanning.

Trivy vulnerability findings are currently report-only. Additional enforcement will be introduced after reviewing the vulnerability baseline.

### Kubernetes

The application is deployed locally using kind.

The Kubernetes configuration includes:

- FastAPI Deployment.
- ClusterIP Service.
- ConfigMap.
- Health probes.
- Resource requests and limits.
- Restricted container security settings.

### Infrastructure as Code

Phase 6 introduces Terraform for declarative infrastructure management.

Initial exercises will use local infrastructure resources before introducing cloud infrastructure.

## 10. Development Roadmap

| Phase | Focus | Status |
|---|---|---|
| Phase 1 | Development environment setup | Complete |
| Phase 2A | Git, GitHub, and documentation | Complete |
| Phase 2B | FastAPI application foundation | Complete |
| Phase 3 | Docker and Docker Compose | Complete |
| Phase 4 | Security scanning and GitHub Actions | Complete |
| Phase 5 | Kubernetes with kind | Complete |
| Phase 6 | Terraform and Infrastructure as Code | In Progress |
| Phase 7 | Cloud deployment and public access | Planned |
| Phase 8 | Production security and operational readiness | Planned |

### Current Focus — Phase 6

- Install and verify Terraform.
- Learn Terraform configuration and state management.
- Practice infrastructure provisioning locally.
- Introduce variables, outputs, and reusable modules.
- Implement Terraform validation and security scanning.
- Integrate infrastructure changes into GitHub workflows.
- Prepare for future cloud deployment.

### Application Development Backlog

The following features remain planned independently of infrastructure learning:

- Responsive frontend.
- Public tennis court data integration.
- PostgreSQL application persistence.
- Authentication and player profiles.
- Player matching and match scheduling.
- Notifications.

## 11. Cloud Deployment Goal

A future phase will make DC Tennis Connect accessible through a public HTTPS URL.

The target is a responsive application usable from desktop and mobile browsers.

Cloud deployment planning will include:

- Appropriate hosting infrastructure.
- Public HTTPS access and DNS.
- Database persistence.
- Secure configuration and secret management.
- Automated deployment workflows.
- Logging, monitoring, and recovery.
- Security validation before public access.

Kubernetes and Terraform will be evaluated as deployment options, but the application will not require a managed Kubernetes service if a simpler hosting approach is more economical.

## 12. Security and Privacy

The project follows secure development practices, including:

- Least-privilege access.
- Non-root container execution.
- Automated testing and security scanning.
- Protection of credentials and environment files.
- Input validation.
- Security findings documentation.
- Review of infrastructure changes.

The current environment is intended for local development and learning.

The application is not yet approved for public production deployment.

### Security Documentation

- `docs/security/security-policy.md`
- `docs/runbooks/security-findings.md`

Outstanding vulnerabilities remain tracked for future investigation and remediation.

## 13. Cost Considerations

The project prioritizes free and open-source technologies.

Current local development does not require paid cloud infrastructure.

Google Maps directions use standard URLs rather than paid mapping APIs.

Potential future costs include:

- Cloud hosting.
- Database hosting and storage.
- Domain registration.
- SMS delivery.
- Third-party data services.

Free tiers and trial offerings will be evaluated before provisioning cloud resources.

Any paid service must be evaluated and approved before implementation.

## 14. Documentation and Maintenance

The project maintains separate documentation for:

- Application requirements.
- System architecture.
- Kubernetes architecture.
- Security policies.
- Security findings.
- Infrastructure configuration.
- Operational procedures.

Documentation will be updated as new features, technologies, and deployment environments are introduced.

Changes should be reviewed and version-controlled through GitHub pull requests.

## 15. Current Project Status

**Current Phase:** Phase 6 — Terraform and Infrastructure as Code

**Completed:** FastAPI foundation, Docker, automated testing, security scanning, GitHub Actions, and local Kubernetes deployment.

**In Progress:** Terraform installation, configuration, and infrastructure provisioning exercises.

**Next Major Milestone:** Prepare repeatable infrastructure configurations for future cloud deployment.

**Long-Term Goal:** Deliver a secure, publicly accessible web application that helps Washington, D.C. tennis players find courts, coordinate matches, and play more often.