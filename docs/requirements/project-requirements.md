# DC Tennis Connect — Project Requirements

**Current development phase:** Phase 7 — Completed  
**Next development phase:** Phase 8 — PostgreSQL application persistence and real public court data  
**Document scope:** Application-wide requirements and Phase 7 frontend MVP  
**Status:** Living requirements; implementation status is tracked separately

## 1. Purpose

DC Tennis Connect will provide a centralized platform for discovering public tennis courts, reviewing publicly available court schedules, coordinating hitting sessions, and finding compatible hitting partners in Washington, D.C.

The application will use reliable public information to help players identify potential playing times.

Players will schedule matches around published operating hours, reservation information, and known court restrictions.

DC Tennis Connect will not independently reserve public courts or guarantee real-time physical availability.

## 2. Target Users

- Recreational tennis players.
- Players seeking public tennis courts.
- Players looking for compatible hitting partners.
- Players coordinating matches around published court schedules.
- Players unfamiliar with court locations in Washington, D.C.

## 3. Functional Requirements

Requirements FR-001 through FR-011 describe the broader application. FR-012 through FR-018 define the Phase 7 browser interface and reuse the existing backend where applicable. Requirements for later phases remain planned, not implemented.

### FR-001: Responsive Web Access

The application shall support modern desktop and mobile browsers on Windows, macOS, iOS, and Android.

### FR-002: Public Court Directory

The application shall provide a directory of public tennis courts in Washington, D.C.

Court information shall include, where available:

- Court name.
- Physical address.
- Geographic coordinates.
- Number of courts.
- Court surface type.
- Published operating hours.
- Reservation policies.
- Known closures.
- Public information source.

### FR-003: Public Court Schedule and Availability

The application shall display court operating hours, reservation information, and closures obtained from reliable, authorized public sources.

The application shall:

- Display published operating hours by date.
- Display verified reservation availability when publicly accessible.
- Identify courts operating on a first-come, first-served basis.
- Display published closures and restrictions.
- Identify unavailable or outdated scheduling information.
- Record the source and last verification time for schedule information.
- Clearly distinguish published operating hours from confirmed reservation availability.

The application shall not represent a court as guaranteed available solely because it is within published operating hours.

### FR-004: Player Profiles

Users shall be able to create and manage player profiles.

Profiles should include:

- Display name.
- Tennis skill level.
- General playing availability.
- Preferred playing locations.

### FR-005: Skill Ratings

Users shall be able to specify their tennis skill level.

Skill ratings may use self-reported NTRP-style ratings or simplified beginner, intermediate, and advanced classifications.

### FR-006: Hitting Partner Matching

Users shall be able to find compatible hitting partners based on:

- Tennis skill level.
- Preferred playing times.
- Preferred court locations.
- Availability for proposed sessions.

### FR-007: Notifications

The application should support email and SMS notifications for:

- Match invitations.
- Accepted or declined invitations.
- Match scheduling updates.
- Relevant published court schedule changes.

Notification functionality will be introduced incrementally.

### FR-008: Optional Social Features

Future versions may include:

- Social media integration.
- In-app messaging.
- Court ratings and reviews.
- Player connections.

### FR-009: Court Location and Google Maps Navigation

The application shall display the geographic location of each listed tennis court and provide navigation through Google Maps.

Requirements:

- Display court names and physical addresses.
- Store verified geographic coordinates where available.
- Provide a Get Directions option.
- Open Google Maps with the selected court as the destination.
- Support desktop and mobile browsers.
- Use Google Maps URLs without requiring paid mapping APIs.
- Allow users to access directions without creating an account.

### FR-010: Player Match Scheduling

The application shall allow registered players to coordinate hitting sessions using publicly available court scheduling information.

Users shall be able to:

- Select a tennis court.
- Review published operating hours and known restrictions.
- Choose a proposed playing date and time.
- Invite another player.
- Accept or decline match invitations.
- View upcoming scheduled matches.
- Cancel proposed or accepted matches.

The application shall distinguish proposed matches from mutually accepted matches.

Scheduling a match shall not be represented as a confirmed court reservation.

### FR-011: Court Schedule Data Management

The application shall support maintaining court scheduling information obtained from authorized public sources.

The system shall support:

- Recording original data sources.
- Importing or updating published schedules.
- Recording verification timestamps.
- Detecting changes where feasible.
- Flagging outdated or missing information.
- Preventing unsupported claims of real-time availability.

Automated data retrieval may be introduced after verifying that the relevant source permits it.

### Phase 7 — Frontend Interface Requirements

The following requirements apply to the initial server-rendered frontend using FastAPI and Jinja2. During Phase 7, the interface uses fictional court records; real court data, database persistence, authentication, and player scheduling remain deferred. Existing JSON API routes must remain functional.

### FR-012: Frontend Homepage

The application shall provide a browser-accessible homepage introducing DC Tennis Connect and its court discovery functionality.

### FR-013: Court Directory Interface

The application shall display tennis court information using the existing backend court service layer.

### FR-014: Court Search and Filtering

Users shall be able to search and filter available court records using supported court attributes.

The interface shall not imply that filtering by public access or operating hours guarantees physical court availability.

### FR-015: Court Detail Pages

Users shall be able to view individual court details, including court name, location, available facility information, and relevant scheduling information.

Unavailable or unverified fields shall be clearly identified or omitted as appropriate.

### FR-016: Google Maps Navigation

Court detail pages shall expose the Google Maps directions capability specified by FR-009, reusing the existing backend navigation URL generation functionality rather than implementing a second mapping mechanism. No paid Google Maps API is required for the initial implementation.

### FR-017: Frontend Error Handling

The interface shall provide understandable messages for:

- Missing court records.
- Empty search results.
- Invalid user input.
- Unavailable application data.

### FR-018: Progressive Enhancement

Core court discovery functionality shall remain usable without client-side JavaScript where practical.

JavaScript may enhance interactions without becoming a requirement for basic navigation.

## 4. Nonfunctional Requirements

### NFR-001: Security

The application shall follow secure development practices, including authentication, authorization, input validation, and protection of user information.

### NFR-002: Maintainability

Application components shall be organized into logical modules.

### NFR-003: Portability

The application shall support local development and future containerized deployment.

### NFR-004: Reliability and Data Accuracy

The application shall distinguish published operating hours from verified reservation availability.

Outdated, missing, or unverified scheduling information shall be clearly identified.

### NFR-005: Testability

Core application functionality shall support automated unit and integration testing.

### NFR-006: Observability

Future deployments should support logging, health monitoring, and troubleshooting.

### NFR-007: Mapping and Navigation Compatibility

Google Maps navigation shall function across supported desktop and mobile browsers without requiring paid mapping APIs for the MVP.

### NFR-008: Data Source Transparency

Court scheduling information shall identify its original source and last verification time.

### NFR-009: Scheduling Integrity

The application shall:

- Reject proposed match times in the past.
- Prevent scheduling outside known operating hours.
- Prevent scheduling during verified closures.
- Identify conflicts with a player's accepted matches.
- Flag known reservation conflicts.
- Warn users when availability is unknown.

An internally scheduled match shall not be treated as proof of a court reservation.

### NFR-010: Privacy

Player profiles, match invitations, and availability preferences shall be protected through appropriate access controls.

The application shall minimize the collection and storage of precise user location information.

### Phase 7 — Frontend Nonfunctional Requirements

The following requirements supplement the application-wide requirements above. NFR-011 refines FR-001 for frontend layouts; NFR-013 supplements NFR-001; NFR-014 supplements NFR-002; and NFR-015 supplements NFR-005.

### NFR-011: Responsive Design

The frontend shall adapt its layout and controls to modern desktop and mobile browsers, consistent with FR-001.

### NFR-012: Accessibility

The frontend shall use semantic HTML, keyboard-accessible controls, visible focus indicators, readable text, and appropriately labeled form elements.

WCAG 2.2 Level AA shall be the target for future accessibility verification.

### NFR-013: Frontend Security

The frontend shall escape untrusted content, validate query parameters, and avoid exposing secrets or internal application details.

### NFR-014: Frontend Maintainability

Templates, stylesheets, static assets, and frontend routes shall be organized into separate logical components.

### NFR-015: Frontend Testability

Frontend routes, template rendering, filtering, and error responses shall be supported by automated tests.

## 5. MVP Scope

### 5.1 Broader Application MVP (Planned)

The broader application MVP shall include:

- Responsive web application.
- Public tennis court directory.
- Court names, addresses, and verified coordinates where available.
- Published court operating hours.
- Known closures and reservation policies.
- Court scheduling classifications.
- Public schedule source attribution.
- Google Maps directions.
- Basic court and date selection.

The initial MVP may use clearly labeled sample scheduling information during development.

The next functional iteration will introduce:

- Player registration and profiles.
- Skill ratings.
- Player availability preferences.
- Match invitations and acceptance.
- Basic player match scheduling.

Later iterations will introduce notifications, enhanced matching, and automated schedule updates.

### 5.2 Phase 7 Frontend MVP (Current Milestone)

Phase 7 uses the existing fictional court data and does not require real schedules, persistent court records, player accounts, or match scheduling. Scheduling fields shall only be shown when present and clearly identified as sample, verified, or unknown.

The Phase 7 frontend MVP is complete when:

1. The homepage renders successfully.
2. The court directory displays existing fictional court records.
3. Search and filtering operate correctly.
4. Individual court pages display available details.
5. Google Maps navigation links work.
6. Missing court records produce an appropriate response.
7. The interface works at desktop and mobile viewport sizes.
8. Existing JSON API endpoints remain functional.
9. Automated frontend and existing backend tests pass.
10. Docker and Kubernetes deployments remain compatible.

## 6. Constraints

- Prioritize free and open-source technologies.
- Minimize infrastructure and external service costs.
- Develop locally before deploying publicly.
- Use authorized public court information.
- Respect third-party data access and usage restrictions.
- Do not assume published schedules represent real-time occupancy.
- Do not represent a player-scheduled match as a reserved court.
- Use Google Maps URLs for navigation.
- Do not require paid mapping APIs for the MVP.
- Avoid unnecessary collection of personal location information.
- Require explicit approval before introducing paid services.

## 7. Acceptance Criteria

The criteria below cover the broader application roadmap. Criteria involving real public schedules or player accounts are not prerequisites for Phase 7; Phase 7 completion is governed by Section 5.2.

### AC-001: Court Discovery

Users can browse public tennis courts in Washington, D.C.

### AC-002: Court Information

Users can view court names, addresses, and available facility information.

### AC-003: Public Court Schedule

Users can view published operating hours and known closures for a selected date.

### AC-004: Availability Transparency

Users can distinguish published operating hours, verified reservation availability, first-come-first-served access, and unknown availability.

### AC-005: Data Source Attribution

Court scheduling information identifies its original source and last verification time.

### AC-006: Court Location

Users can view court addresses and verified coordinates where available.

### AC-007: Google Maps Navigation

Users can open Google Maps directions to a selected tennis court.

### AC-008: Player Match Scheduling

Registered users can propose a court, date, and time to another player.

### AC-009: Match Confirmation

A proposed match becomes accepted only after the invited player agrees.

### AC-010: Reservation Transparency

The application clearly communicates that scheduling a match does not reserve a public tennis court.

### AC-011: Scheduling Validation

The application rejects invalid proposed sessions and identifies known scheduling conflicts.

### AC-012: Cross-Platform Support

Court discovery, published schedules, and Google Maps navigation work on supported desktop and mobile browsers.

### AC-013: Cost Control

Local development operates without requiring paid cloud infrastructure or mapping API subscriptions.

### 7.1 Phase 7 Acceptance Mapping

| Phase 7 deliverable | Requirements | Verification |
|---|---|---|
| Homepage | FR-012 | Browser route renders successfully |
| Directory and filtering | FR-013, FR-014 | Fictional records display; supported filters work; empty results handled |
| Court detail pages | FR-015 | Existing record renders; missing record handled |
| Directions | FR-009, FR-016 | Valid Google Maps destination link for supported court data |
| Error handling | FR-017 | Missing records and invalid inputs produce understandable responses |
| Progressive enhancement | FR-018 | Core court discovery works without JavaScript where practical |
| Responsive and accessible interface | FR-001, NFR-011, NFR-012 | Desktop/mobile and keyboard checks |
| Security and maintainability | NFR-013, NFR-014 | Template and route review; no secrets exposed |
| Regression and deployment compatibility | NFR-015 | Frontend and existing API tests pass; Docker and kind verified |

Additional acceptance criteria will be defined as implementation progresses.