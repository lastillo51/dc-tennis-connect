# DC Tennis Connect

## Project Overview

DC Tennis Connect is a web-based application designed to help tennis players in Washington, D.C. discover public tennis courts, review published court schedules, coordinate hitting sessions, and obtain directions using Google Maps.

The application will use reliable, publicly available court information to help players identify potential playing times.

Players will be able to organize matches around published operating hours, reservation information, and known court restrictions.

DC Tennis Connect will not independently reserve public courts or guarantee that a court is physically unoccupied.

## Project Goals

**Application Goal:** Simplify tennis planning by combining public court discovery, published scheduling information, player matching, match coordination, and navigation.

**Learning Goal:** Gain hands-on experience implementing DevSecOps technologies throughout the software development lifecycle.

## Target Users

- Recreational tennis players in Washington, D.C.
- Players looking for public tennis courts.
- Players searching for compatible hitting partners.
- Players coordinating matches around court schedules.
- Players unfamiliar with local court locations.

## Planned Features

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

## How the Application Will Work

1. A player searches for a public tennis court.
2. The application displays the court's location, published operating hours, reservation information, and known restrictions.
3. The player reviews potential playing times.
4. The player selects a court, date, and time for a proposed hitting session.
5. The player invites a compatible hitting partner.
6. The invited player accepts or declines.
7. Accepted matches appear in both players' schedules.
8. Players use Google Maps to navigate to the selected court.

Scheduling a match through DC Tennis Connect does not constitute an official court reservation.

Published operating hours do not guarantee that a court is physically unoccupied.

## Court Availability Approach

Court scheduling information will come from reliable, authorized public sources.

Potential sources include:

- DC Department of Parks and Recreation.
- DC Open Data.
- Official court reservation platforms where information is publicly accessible and reuse is permitted.
- Published facility operating schedules and closure notices.

The application will distinguish:

- Published operating hours.
- Verified reservable time slots.
- Published reservations.
- First-come, first-served access.
- Known closures.
- Unknown availability.

The MVP will initially use manually verified public information.

Automated updates may be introduced after confirming that the relevant sources permit programmatic access.

## Technology Stack

| Category | Technology |
|---|---|
| Version Control | Git and GitHub |
| Backend | Python and FastAPI |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| Database | PostgreSQL |
| Containers | Docker Engine and Docker Compose |
| Infrastructure as Code | Terraform |
| Container Orchestration | Kubernetes and kind |
| Container Security | Trivy |
| Static Security Analysis | Semgrep |
| CI/CD | GitHub Actions |
| Testing | Pytest |
| Navigation | Google Maps URLs |

## Development Environment

- Ubuntu Desktop 26.04.1 LTS.
- VMware Workstation Pro.
- Visual Studio Code.
- Local-first development environment.

## Project Status

Phase 1: Development environment and directory structure completed.

Phase 2A: Git, GitHub, and project documentation in progress.

## Development Roadmap

1. Establish project documentation and Git workflows.
2. Build the court directory and published schedule display.
3. Implement Google Maps navigation.
4. Introduce player profiles and match scheduling.
5. Containerize the application.
6. Introduce automated testing and security scanning.
7. Deploy to a local Kubernetes cluster.
8. Explore Terraform infrastructure provisioning.
9. Expand player matching, notifications, and operational features.

## Cost Considerations

The project prioritizes free and open-source technologies.

Local development will not require paid cloud infrastructure.

Google Maps directions will use standard URLs rather than paid mapping APIs.

External hosting, SMS delivery, and certain third-party data services may introduce costs in later phases.

Any paid service must be evaluated and approved before implementation.