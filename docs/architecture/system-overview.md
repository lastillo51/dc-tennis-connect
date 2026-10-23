# DC Tennis Connect — System Architecture

## 1. Architecture Overview

DC Tennis Connect will use a Python FastAPI application, PostgreSQL database, and responsive web interface.

The application will combine publicly available tennis court scheduling information with player-generated match scheduling.

The system will not independently reserve public courts or guarantee physical court availability.

## 2. Core Components

### Web Interface

The responsive web interface will support:

- Public tennis court directory.
- Court details and locations.
- Published operating hours and availability classifications.
- Court and date selection.
- Player profiles.
- Match invitations and scheduling.
- Google Maps navigation.

### Backend

Python and FastAPI will provide:

- Court directory endpoints.
- Court schedule retrieval.
- Schedule data validation.
- Player profile management.
- Match scheduling and invitation workflows.
- Authentication and authorization.
- Google Maps destination link generation.

### PostgreSQL Database

The database will maintain separate records for:

- Tennis courts.
- Court locations.
- Court operating hours.
- Published closures and reservation information.
- Public data sources.
- Schedule verification timestamps.
- Player profiles.
- Player availability preferences.
- Match invitations.
- Scheduled matches.

Public court schedules and player-created matches shall remain logically separate.

An accepted player match shall not automatically change a public court's reservation availability status.

## 3. Public Court Data Management

### Data Sources

The application will prioritize reliable, authorized public information from sources such as:

- DC Department of Parks and Recreation.
- DC Open Data.
- Official public reservation systems where permitted.
- Published facility schedules and closure notices.

The availability and permitted use of each source must be verified before integration.

### Data Collection

The initial implementation may use manually verified public court information.

Automated collection may be introduced after confirming that the source permits programmatic access.

### Data Validation

Court schedule information will include, where available:

- Court identifier.
- Published operating hours.
- Date-specific restrictions.
- Reservation information.
- Closure information.
- Original source.
- Last verification timestamp.

The application shall distinguish operating hours from confirmed reservation availability.

### Data Freshness

Outdated or unverified schedule information shall be clearly identified.

The system shall not imply real-time accuracy when the source does not support it.

## 4. Player Match Scheduling

Players will coordinate hitting sessions around published court information.

### Scheduling Workflow

1. A player selects a court.
2. The application displays published operating hours and known restrictions.
3. The player selects a proposed date and time.
4. The application validates the proposed time against known restrictions.
5. The player invites another registered player.
6. The invited player accepts or declines.
7. Accepted matches appear in both players' schedules.
8. Players can access Google Maps directions to the selected court.

### Match Status

Proposed match statuses include:

- Pending.
- Accepted.
- Declined.
- Cancelled.

A scheduled match represents an agreement between players, not a court reservation.

### Scheduling Validation

The application shall:

- Reject past match times.
- Reject sessions outside known operating hours.
- Reject sessions during verified closures.
- Flag known reservation conflicts.
- Identify overlapping accepted matches for the same player.
- Display warnings when court availability is unknown.

A first-come, first-served court may still be occupied when players arrive.

## 5. Google Maps Navigation

Each court listing will provide an address and Get Directions option.

The application will use Google Maps URLs to open external navigation.

No paid Google Maps API is required for the initial implementation.

The application will not calculate routes or require users to share their precise location.

## 6. Development Environment

Development will take place locally using:

- Ubuntu Desktop 26.04.1 LTS.
- VMware Workstation Pro.
- Git and GitHub.
- Visual Studio Code.
- Python and FastAPI.
- PostgreSQL.

## 7. DevSecOps Architecture

### Docker

Docker Engine and Docker Compose will package and run the application and database locally.

### Terraform

Terraform will support infrastructure-as-code learning and repeatable infrastructure provisioning.

### Kubernetes

A local kind cluster will support Kubernetes deployment exercises.

### Trivy

Trivy will scan container images, dependencies, and supported infrastructure configurations.

### Semgrep

Semgrep will perform static application security analysis.

### GitHub Actions

GitHub Actions will automate testing and security checks in later phases.

### Development Dependency Management and Compatibility

DC Tennis Connect will maintain version-controlled Python dependencies to support reproducible development, automated testing, and future CI/CD integration.

Python dependencies are currently managed using a project-specific virtual environment (`.venv`) and a `requirements.txt` file.

#### Current Development Dependencies

The following dependency versions were verified during Phase 2B:

| Dependency | Version |
|---|---|
| Python | 3.14 |
| FastAPI | 0.159.1 |
| Starlette | 1.9.0 |
| HTTPX | 0.28.1 |
| Pytest | 9.1.1 |

These versions represent the development environment at the time of verification and may change as the project evolves.

#### Known Dependency Compatibility Warning

During Phase 2B, automated testing produced the following warning:

`StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead.`

The warning originates from Starlette's testing integration, which FastAPI uses through `TestClient`.

The current automated tests execute successfully despite the warning.

The dependency validation command:

`python -m pip check`

returned:

`No broken requirements found.`

This indicates that the installed packages satisfy their declared dependency requirements. It does not guarantee compatibility with future releases.

#### Current Decision

The project will retain the currently working dependency versions until the recommended migration path has been reviewed and tested.

No dependency changes will be introduced solely to suppress the warning.

The warning is classified as a **known development dependency compatibility issue**, not a confirmed security vulnerability.

#### Planned Follow-Up Actions

1. Review official FastAPI and Starlette release notes and migration guidance.
2. Determine whether HTTPX2 is the recommended replacement for the installed versions.
3. Evaluate the impact of any migration on existing automated tests.
4. Test dependency changes within the Python virtual environment.
5. Run the complete Pytest suite after dependency updates.
6. Run `python -m pip check` to verify declared dependency compatibility.
7. Update `requirements.txt` with the validated dependency versions.
8. Remove this known issue once the warning has been resolved and regression tests pass.

#### Future DevSecOps Integration

As the project evolves, dependency management will be integrated into the DevSecOps workflow.

Future GitHub Actions pipelines should:

- Install dependencies from the version-controlled dependency manifest.
- Run automated tests.
- Check dependency compatibility.
- Execute security scans using Trivy and Semgrep where applicable.
- Report failures and relevant warnings before changes are merged.

Dependency upgrades will be introduced through feature branches and reviewed through GitHub pull requests.

Significant compatibility issues will be documented until resolved.


## 8. Security and Privacy

The application will follow these principles:

- Least privilege.
- Secure authentication and authorization.
- No credentials committed to Git.
- Validation of user-provided scheduling information.
- Protection of player availability and match details.
- Secure handling of public data imports.
- Safe construction of external navigation URLs.
- Minimal collection of precise location information.

## 9. Future Enhancements

Potential future improvements include:

- Automated public schedule synchronization.
- Court schedule change notifications.
- Enhanced player matching.
- Email and SMS notifications.
- Interactive court maps.
- Distance-based court search.
- Native mobile applications.

## 10. Architecture Status

This document describes the proposed architecture.

Data source feasibility, integration methods, and implementation details will be validated before development.