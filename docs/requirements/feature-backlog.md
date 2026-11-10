# DC Tennis Connect — Frontend Architecture

> **Project stage:** Phase 7 — Frontend Development (Exercise 5: quality, security, and deployment compatibility)  
> **Implementation:** Server-rendered FastAPI/Jinja2 frontend using fictional court data  
> **Deployment:** Local development and local Docker/kind verification; not approved for public deployment

## 1. Purpose and Scope

This document describes the **implemented** frontend architecture of DC Tennis Connect and distinguishes it from future functionality. The frontend helps users browse fictional sample tennis courts, search names and addresses, filter public-access courts, view details, and open Google Maps directions.

The application does not reserve courts or verify real-time occupancy. Published hours and availability classifications must not be presented as guarantees that a court is unoccupied. Real Washington, D.C. public court data, player accounts, and match scheduling are outside the current frontend foundation.

## 2. Technology Stack and Principles

| Technology | Current responsibility |
|---|---|
| Python / FastAPI | Application, route handling, parameter validation, and service integration |
| Jinja2 / HTML5 | Server-rendered pages and semantic structure |
| CSS3 | Responsive layout, visual design, and focus styling |
| Pytest / FastAPI TestClient | Web route, rendering, integration, and security regression tests |
| JavaScript | Optional future progressive enhancement; not required by current pages |

Architecture principles:

- Reuse existing API schemas and services rather than duplicating court records or business logic.
- Keep route handling, data retrieval, URL generation, templates, and styling separate.
- Preserve the existing JSON API contracts while introducing HTML routes.
- Prefer native links and forms, accessible semantics, and minimal dependencies.
- Treat external court data and generated navigation links as security-sensitive inputs.
- Make unknown or unverified availability explicit.

## 3. Implemented File Structure

```text
app/
├── main.py
├── api/
│   ├── routes/
│   │   └── courts.py
│   ├── schemas/
│   │   └── court.py
│   └── services/
│       ├── court_service.py
│       ├── maps_service.py
│       └── sample_courts.py
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
    ├── test_web.py
    ├── test_court_directory_web.py
    ├── test_court_detail_web.py
    ├── test_frontend_accessibility.py
    ├── unit/
    │   └── test_maps_service.py
    └── integration/
        └── test_api.py
```

The accessibility test file reflects Exercise 5 work and should be listed as implemented only after it exists and its tests pass. Additional existing application and test files are omitted from this focused tree. Dedicated `errors/` templates and `static/js/main.js` remain **planned**, not assumed to exist.

## 4. Application Components

| Component | File | Responsibility |
|---|---|---|
| Application entry point | `app/main.py` | Registers routers and mounts `/static` |
| Frontend routes | `app/web/routes.py` | Homepage, court directory, and detail pages |
| Court API | `app/api/routes/courts.py` | Existing JSON endpoints, including `list_courts()` |
| Court service | `app/api/services/court_service.py` | `get_all_courts()`, `get_court_by_id()`, `search_courts()` |
| Court schema | `app/api/schemas/court.py` | Validated court attributes and nested `CourtLocation` |
| Sample data | `app/api/services/sample_courts.py` | Fictional in-memory court records |
| Maps service | `app/api/services/maps_service.py` | `build_google_maps_url(court.location)` |
| Base template | `app/templates/base.html` | Shared layout, navigation, and static asset reference |
| Page templates | `app/templates/home.html`, `app/templates/courts/*.html` | User-facing pages |
| Stylesheet | `app/static/css/styles.css` | Responsive and accessibility-related styles |

The correct address attribute is `court.location.address`, not `court.address`. The frontend uses `search_courts()` from the service layer; the API router's `list_courts()` remains a separate JSON endpoint.

## 5. Routing and Data Flow

| Route | Response | Purpose |
|---|---|---|
| `/web` | HTML | Homepage |
| `/web/courts` | HTML | Searchable, filterable court directory |
| `/web/courts/{court_id}` | HTML | Individual court details and directions |
| `/static/css/styles.css` | CSS | Stylesheet |
| `/courts/` | JSON | Existing court directory API |
| `/health` | JSON | Health endpoint |
| `/docs` | HTML | FastAPI interactive API documentation |

A browser request follows this flow:

1. FastAPI validates the route path and query parameters.
2. The frontend route calls the shared court service; the service reads fictional sample records.
3. For a detail page, the route retrieves the selected court and calls `build_google_maps_url(court.location)`.
4. The route supplies court data and the generated directions URL to Jinja2.
5. Jinja2 renders HTML and the browser requests the local CSS asset.

The frontend does **not** call its own JSON API over HTTP or maintain a duplicate court database. The API and frontend share the same models and services.

## 6. Court Directory and Detail Pages

### Court directory

- Displays the fictional court records currently available through the service layer.
- Supports case-insensitive search across court names and `court.location.address`.
- Supports public-only filtering using `court.public_access`.
- Limits the search query length through FastAPI validation.
- Provides a no-results state and links to individual detail pages.

### Court details

- Displays name, nested address, number of courts, public-access status, availability classification, reservation requirement, and operating hours when present.
- Returns HTTP 404 for unknown court IDs and HTTP 422 for nonnumeric IDs.
- Displays explicit availability disclaimers rather than suggesting real-time occupancy information.
- Generates a Google Maps directions link from the existing Maps service. The optional model field `court.google_maps_url` need not be populated in the fictional records.

Google Maps navigation uses a fixed HTTPS directions endpoint and URL-encoded destination data; no Google Maps API key is needed for this URL-based approach. Fictional destinations may not resolve to real facilities.

## 7. Accessibility and Responsive Design

The frontend uses semantic HTML, native form controls, visible focus styles, and responsive CSS. Phase 7 Exercise 5 includes verification of a skip-navigation link, form labels, heading hierarchy, keyboard navigation, and representative viewport widths (375px, 768px, and 1280px).

Accessibility remains an ongoing review area. Basic HTML assertions and manual keyboard checks do not constitute a complete WCAG conformance audit. Confirm the skip link and any new accessibility tests are actually implemented and passing before marking those specific checks complete.

## 8. Error Handling

- Unknown court records return HTTP 404.
- Invalid typed parameters or overlong search queries return HTTP 422.
- Empty searches render a normal HTML empty state.
- Missing operating hours are displayed as unavailable, not inferred.
- Standard FastAPI error responses may currently be JSON rather than styled HTML pages.

Dedicated user-friendly 404 and 500 templates are planned improvements. Public deployment must not expose detailed application tracebacks or sensitive configuration.

## 9. Frontend Security

Current controls and verification targets include:

- Jinja2 HTML autoescaping for court names and addresses; avoid unreviewed `safe` filters.
- FastAPI validation for search parameters and court IDs.
- A trusted Maps service that constructs the URL rather than accepting arbitrary redirect destinations.
- `target="_blank"` links paired with `rel="noopener noreferrer"`.
- Static assets served only from the intended `app/static/` directory.
- Automated tests for escaping, input validation, and navigation behavior.
- Semgrep static analysis and Trivy container scanning.

**Tracked security finding:** `SEC-FE-001` concerns the dynamic Jinja2 `href="{{ google_maps_url }}"`. The fixed-domain URL generator supports a potential false-positive assessment, but the finding must retain its evidence-supported disposition in `docs/runbooks/security-findings.md`; passing tests alone do not close it.

The Phase 7 container scan also records vulnerability findings requiring triage. Security headers, CSP enforcement, authentication, and authorization need further assessment before public deployment.

## 10. Testing and Verification

| Test area | Relevant file or procedure |
|---|---|
| Homepage | `app/tests/test_web.py` |
| Court directory, search, filtering | `app/tests/test_court_directory_web.py` |
| Detail pages, missing records, Maps link, escaping | `app/tests/test_court_detail_web.py` |
| Maps URL construction | `app/tests/unit/test_maps_service.py` |
| Existing JSON API | `app/tests/integration/test_api.py` |
| Accessibility smoke checks | `app/tests/test_frontend_accessibility.py` (verify file and passing tests) |
| Browser responsiveness and keyboard behavior | Manual desktop/tablet/mobile verification |
| Security | Semgrep, Trivy, dependency consistency, findings register |

Run the complete application suite with `python -m pytest app/tests/ -q` and dependency consistency with `python -m pip check`. The last explicitly reported regression baseline was **42 passing tests with one Starlette deprecation warning**; update the recorded count only from a newer completed run.

## 11. Local Deployment Compatibility

The frontend runs inside the existing FastAPI process. The Dockerfile copies `app/` into the runtime image, including templates and CSS, and the local kind deployment exposes the same application through a Kubernetes Service.

Phase 7 Exercise 5 verifies the frontend routes and CSS in a local Docker image and in the `dc-tennis` kind cluster. Preserve the non-root container security configuration, health probes, resource limits, and API behavior. A live `kubectl set image` change must be reconciled with the Git-managed Deployment manifest or rolled back after testing.

Terraform currently provides a local infrastructure-as-code learning foundation; this frontend work does not imply production cloud infrastructure has been provisioned.

## 12. Known Limitations and Future Enhancements

- Fictional, in-memory court records; no live public DC court data or application database persistence.
- Published court availability is not real-time occupancy or an official reservation.
- No player authentication, profiles, matching, invitations, or scheduling yet.
- No dedicated styled 404/500 pages or JavaScript framework required for current functionality.
- Security findings and public-deployment controls remain under review.
- Future work includes verified public data sources and attribution, PostgreSQL persistence, interactive maps, player coordination, notifications, and public HTTPS deployment.

## 13. Related Documentation

- `README.md`
- `docs/architecture/system-overview.md`
- `docs/architecture/kubernetes-overview.md` (if present)
- `docs/security/security-policy.md`
- `docs/runbooks/security-findings.md`
- Project requirements and feature backlog documents

Update this architecture document when routes, data sources, security decisions, deployment architecture, or frontend capabilities materially change. Phase 7 remains **in progress** until final review, pull request, and merge.