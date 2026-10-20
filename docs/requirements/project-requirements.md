# DC Tennis Connect — Project Requirements

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

## 5. MVP Scope

The initial technical MVP shall include:

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

Additional acceptance criteria will be defined as implementation progresses.