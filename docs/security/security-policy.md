# DC Tennis Connect — DevSecOps Security Policy

**Current project phase:** Phase 7 — Frontend Development  
**Deployment status:** Local development; not approved for public production deployment.

## 1. Purpose

This document establishes security requirements and development practices for DC Tennis Connect. It covers application development, frontend rendering, infrastructure management, automated testing, vulnerability management, and deployment. The policy evolves as features and technologies are introduced.

## 2. Scope

| Component | Scope |
|---|---|
| Backend | Python, FastAPI, application services, and JSON APIs |
| Frontend | Jinja2, HTML, CSS, JavaScript, web routes, templates, and static assets |
| Dependencies | Python packages and third-party libraries |
| Containers | Docker images and Docker Compose |
| Database | Local PostgreSQL and future application persistence |
| Source control | Git, GitHub, branches, and pull requests |
| CI/CD | GitHub Actions, Pytest, Semgrep, and Trivy |
| Infrastructure | Local Kubernetes with kind and Terraform configurations |
| User data | Future authentication, profiles, availability, and scheduling information |

Update this table when new components are introduced.

## 3. Security Principles

- **Least privilege:** Grant only permissions necessary for each component.
- **Secure by default:** Prefer secure initial configurations.
- **Defense in depth:** Use complementary security controls.
- **Automated verification:** Test and scan changes consistently.
- **Minimal exposure:** Limit unnecessary network access and runtime dependencies.
- **Traceability:** Document findings, remediation decisions, and exceptions.
- **Continuous improvement:** Reassess controls as the application evolves.

## 4. Secure Development Requirements

All application and infrastructure changes should:

1. Use dedicated Git feature branches.
2. Be reviewed through GitHub pull requests.
3. Exclude credentials, tokens, and secrets from commits.
4. Validate external and user-provided input.
5. Apply authentication and authorization as relevant features are introduced.
6. Maintain automated tests for implemented functionality.
7. Review applicable security scans before merging.
8. Update affected architecture, requirements, and security documentation.
9. Preserve existing API behavior unless an intentional, reviewed change is required.

### 4.1 Frontend Application Security — Phase 7

These requirements apply to the planned FastAPI/Jinja2 frontend and must be verified as the corresponding pages and routes are implemented.

**Input handling**

- Validate and constrain search terms, filters, path parameters, and query parameters.
- Treat browser input and external court information as untrusted.
- Avoid reflecting unvalidated values into rendered pages.
- Return understandable errors without disclosing internal implementation details.

**Template rendering**

- Use Jinja2 HTML autoescaping for untrusted content.
- Do not use `|safe`, `Markup`, or equivalent bypasses on untrusted values.
- Do not interpolate untrusted values into executable JavaScript, HTML event handlers, or unsafe URL contexts.
- Keep business logic in application services rather than templates.

**External navigation**

- Generate Google Maps destination links using the existing approved URL-generation logic.
- Do not accept arbitrary user-supplied redirect destinations.
- For links opening new tabs, use `rel="noopener noreferrer"` with `target="_blank"`.
- Do not require collection of the user's precise location for basic directions links.

**Static assets and dependencies**

- Serve approved CSS and JavaScript from controlled application paths.
- Minimize third-party scripts and review new frontend dependencies.
- Do not embed credentials, private configuration, or sensitive user data in public assets.

**Browser security**

- Evaluate Content Security Policy and appropriate response headers as the frontend is implemented; test compatibility before enforcement.
- Use secure cookie settings and CSRF defenses when sessions and state-changing browser forms are introduced.
- Avoid exposing stack traces or debug details in user-facing error pages.

**Accessibility and usability**

- Use semantic HTML, labeled inputs, keyboard-operable controls, and visible focus indicators.
- Provide understandable validation and error messages.
- Review responsive layouts and accessibility against the project's WCAG 2.2 Level AA target.

**Verification**

- Add Pytest coverage for web routes, template rendering, input handling, missing records, and navigation links.
- Continue Semgrep, Trivy container, and GitHub Actions checks.
- Manually inspect rendered output for escaping, safe external links, and accessibility behavior.

## 5. Continuous Integration Security Controls

### 5.1 Current CI Controls

| Control | Technology | Current enforcement |
|---|---|---|
| Application tests | Pytest | Test failures fail the job |
| Dependency consistency | pip | Dependency conflicts fail the job |
| Static application security | Semgrep | Configured `ERROR` findings fail the job |
| Container vulnerability scanning | Trivy | Findings reported; vulnerability gate deferred |
| Terraform formatting and validation | Terraform | Invalid formatting or configuration fails the IaC job |
| Terraform configuration scanning | Trivy | Findings report-only; scanner execution failures fail the job |
| Workflow permissions | GitHub Actions | Read-only repository permissions in documented workflow |
| Workflow execution | GitHub Actions | Timeouts and concurrency controls |

The Terraform checks were added in Phase 6. Verify the current workflow file whenever enforcement settings change.

### 5.2 Planned CI Improvements

- Pin third-party GitHub Actions to verified commit SHAs.
- Reconcile the outstanding Trivy container vulnerability baseline.
- Introduce reviewed, risk-based vulnerability enforcement.
- Improve scan reporting and historical comparison.
- Expand Kubernetes-specific configuration security checks.
- Add frontend route and template tests as Phase 7 features are implemented.

### 5.3 Branch Protection

GitHub branch protection remains deferred during initial solo development. Manual pull-request review is supported by automated CI checks. Reconsider branch protection before public deployment or when additional contributors join.

## 6. Vulnerability Management

### 6.1 Severity and Prioritization

| Severity | Required handling |
|---|---|
| Critical | Investigate promptly and prioritize remediation |
| High | Prioritize investigation and remediation planning |
| Medium | Document and prioritize based on exposure and impact |
| Low | Track during routine dependency and infrastructure maintenance |
| Unknown | Investigate where potential impact warrants review |

Severity alone does not establish exploitability. Assess affected components, exposure, available fixes, and potential impact.

### 6.2 Finding Status

| Status | Definition |
|---|---|
| Open | Finding identified but not yet assessed |
| Investigating | Applicability and impact under review |
| Remediation Planned | Corrective action identified but incomplete |
| Resolved | Remediation implemented and verified |
| Risk Accepted | Risk formally accepted with documented justification |
| False Positive | Finding determined inapplicable based on evidence |

### 6.3 Findings Register

Scan results, remediation evidence, and outstanding risks are maintained in `docs/runbooks/security-findings.md`. This policy defines requirements; the findings register records observations and decisions.

## 7. Security Exceptions and Risk Acceptance

| Field | Required information |
|---|---|
| Finding ID | Unique identifier |
| Affected component | Package, service, or configuration |
| Risk description | Concern and potential impact |
| Justification | Why remediation is deferred |
| Compensating controls | Measures reducing exposure |
| Responsible reviewer | Accountable person |
| Review date | Reassessment date |
| Status | Current exception status |

Review exceptions periodically. Risk acceptance does not mean a vulnerability is resolved and must not conceal findings.

## 8. Container and Infrastructure Security

### 8.1 Docker and Docker Compose

Containerized services should run as non-root where practical, minimize runtime packages, exclude embedded secrets, use maintained base images, limit published ports, separate application and database services, preserve necessary data, and undergo vulnerability scanning.

### 8.2 Planned Container Hardening

- Evaluate multi-stage builds and residual image-layer exposure.
- Pin base images to verified digests.
- Review filesystem permissions and read-only root filesystems.
- Review container resource constraints and capability restrictions.

### 8.3 Kubernetes — Implemented Local Baseline

The Phase 5 kind Deployment uses non-root execution with explicit numeric UID/GID, disabled privilege escalation, dropped Linux capabilities, a `RuntimeDefault` seccomp profile, health probes, and CPU/memory constraints. ConfigMap injection was verified; the demonstration Secret was removed.

Further work includes Kubernetes RBAC, network policies, secure Secret management, and additional configuration scanning before public deployment.

### 8.4 Terraform — Implemented Local Baseline

The Phase 6 configuration uses local demonstration resources, reusable modules, formatting and validation checks, and Trivy IaC scanning. Local state, generated provider directories, and local variable values are excluded from Git; the provider lock file is tracked.

Before cloud provisioning, evaluate encrypted remote state, access controls, locking, recovery, least-privilege cloud identities, and environment separation. IaC scan findings remain report-only under the current policy.

## 9. Secrets and Data Protection

### 9.1 Current Development Practices

- Never commit credentials or tokens to Git.
- Exclude local secret-bearing environment files and Terraform state from version control.
- Apply minimum necessary access to application and database services.
- Avoid exposing sensitive values in logs, CI output, templates, or browser-delivered assets.

### 9.2 Future Application Requirements

Before storing real player information, implement appropriate authentication, authorization, session security, access controls for profiles and schedules, protection of stored/transmitted data, and data retention/deletion practices.

## 10. GitHub Actions Security

Workflows should use least-privilege token permissions, avoid unnecessary secrets, use trusted third-party actions, apply timeouts and concurrency controls, and fail when required tests or scanner execution fails. Pin third-party actions to verified commit SHAs as part of future hardening. Review workflow changes before merging.

## 11. Deployment Security Requirements

The application is currently intended for local development. Before public deployment, review and implement appropriate controls for authentication and authorization, HTTPS, network exposure, production secrets, database security, outstanding vulnerabilities, logging, monitoring, backups, recovery, CI enforcement, browser security, and user data protection.

A successful CI workflow does not automatically authorize production deployment.

## 12. Policy Maintenance and Change Management

### 12.1 Review Triggers

Review this policy when a technology or significant feature is introduced, security architecture changes, CI enforcement changes, new data protection requirements arise, or the application approaches public deployment.

### 12.2 Change Process

1. Identify affected policy sections.
2. Update relevant requirements.
3. Review related architecture and findings documentation.
4. Commit changes on a feature branch.
5. Review through a GitHub pull request.
6. Merge approved changes into `main`.

### 12.3 Policy Review History

| Date | Phase | Change | Status |
|---|---|---|---|
| 2026-10-26 | Phase 4 | Reorganized policy and documented initial DevSecOps controls | Historical entry (previously marked proposed) |
| 2026-11-04 | Phase 7 | Integrated frontend security requirements and updated Phase 5–6 control descriptions | Draft — pending review and merge |

Update status and date when a revision is actually approved and merged.

## 13. Related Documentation

| Document | Purpose |
|---|---|
| `docs/runbooks/security-findings.md` | Scan results, findings, remediation, and risk decisions |
| `docs/architecture/system-overview.md` | Application architecture and security design |
| `docs/architecture/kubernetes-overview.md` | Local Kubernetes architecture |
| `docs/architecture/terraform-overview.md` | Terraform foundation and state approach |
| `docs/architecture/frontend-overview.md` | Phase 7 frontend design (planned document) |
| `.github/workflows/security-ci.yml` | Automated testing and security scanning |
| `docker/Dockerfile` | FastAPI container build configuration |
| `docker/compose.yaml` | Local application and database services |

Add references as new documentation is created.