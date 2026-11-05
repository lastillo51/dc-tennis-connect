# DC Tennis Connect — Frontend Architecture

## 1. Purpose

This document defines the frontend architecture for DC Tennis Connect.

The initial implementation will provide a responsive browser-based interface for discovering tennis courts using the existing FastAPI backend.

The architecture will support future player profiles, match scheduling, and additional application functionality.

## 2. Technology Stack

| Technology | Responsibility |
|---|---|
| FastAPI | Web routes and application integration |
| Jinja2 | Server-rendered HTML templates |
| HTML5 | Semantic page structure |
| CSS3 | Responsive presentation |
| JavaScript | Optional progressive enhancement |
| Pytest | Automated frontend verification |

## 3. Architecture Principles

The frontend shall:

- Reuse existing backend services.
- Keep presentation logic separate from business logic.
- Preserve existing JSON API endpoints.
- Avoid unnecessary dependencies.
- Support progressive enhancement.
- Remain modular and extensible.
- Follow established security practices.

## 4. Proposed Directory Structure

```text
app/
├── api/
├── services/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── courts/
│   │   ├── index.html
│   │   └── detail.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
├── web/
│   └── routes.py
└── tests/
```

This structure is proposed and will be adjusted to match the existing application layout before implementation.

## 5. Routing

| Route | Purpose |
|---|---|
| `/web` | Homepage |
| `/web/courts` | Court directory |
| `/web/courts/{court_id}` | Court details |
| `/courts/` | Existing JSON API |
| `/health` | Application health |
| `/docs` | API documentation |

Frontend routes shall not unintentionally replace or break existing API endpoints.

## 6. Data Flow

1. A browser requests a frontend page.
2. FastAPI processes the web route.
3. The route obtains court information from the shared service layer.
4. The route passes validated presentation data to Jinja2.
5. Jinja2 renders the HTML response.
6. The browser loads the associated CSS and optional JavaScript.
7. The user interacts with court listings and navigation links.

The frontend will not maintain a separate duplicate court database.

## 7. Court Directory

The directory will display available information from the existing court schema.

The initial implementation will use fictional sample records.

Search and filtering will use supported service-layer capabilities.

Missing or unverified court information shall not be presented as confirmed.

## 8. Court Details and Navigation

Each court detail page will display available court attributes.

Where a valid destination is available, the page will provide a Google Maps directions link.

The frontend will reuse the existing backend navigation URL generation logic.

The initial implementation will not require a Google Maps API key.

## 9. Responsive Design

The frontend will use a mobile-first layout approach.

Primary considerations include:

- Readable typography.
- Responsive court listings.
- Touch-friendly controls.
- Accessible navigation.
- Appropriate spacing.
- Consistent visual hierarchy.

The interface will be tested at representative mobile, tablet, and desktop viewport sizes.

## 10. Error Handling

The frontend will provide understandable responses for:

- Invalid court identifiers.
- Missing court records.
- Empty search results.
- Unavailable application data.
- Unexpected server errors.

Detailed internal errors shall not be exposed to end users.

## 11. Security

The frontend will use:

- Jinja2 autoescaping.
- Validated request parameters.
- Safe external navigation links.
- Controlled static assets.
- Appropriate browser security practices.
- Automated tests and security scanning.

Additional security controls will be introduced when authentication and state-changing forms are implemented.

## 12. Testing Strategy

Automated tests will verify:

- Homepage rendering.
- Court directory rendering.
- Search and filtering.
- Court detail pages.
- Missing-record responses.
- Google Maps links.
- Preservation of existing JSON API behavior.

Manual verification will cover responsive layouts, accessibility, and browser usability.

## 13. Deployment Compatibility

The frontend will run within the existing FastAPI application.

Docker and Kubernetes configurations will be reviewed to ensure templates and static assets are included in deployment images.

Terraform infrastructure changes are not expected during the initial frontend implementation.

## 14. Future Enhancements

- Authentication and player profiles.
- Player matching and scheduling.
- Database-backed court records.
- Interactive maps.
- Additional frontend interactivity.
- Public HTTPS deployment.
- Accessibility improvements.

## 15. Related Documentation

- `README.md`
- `docs/architecture/system-overview.md`
- `docs/architecture/kubernetes-overview.md`
- `docs/security/security-policy.md`
- Project requirements document.
- Feature backlog.