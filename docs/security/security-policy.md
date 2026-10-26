# DC Tennis Connect — DevSecOps Security Policy

## 1. Purpose

This document establishes the security requirements and development practices for DC Tennis Connect.

The policy supports secure application development, infrastructure management, automated testing, vulnerability management, and deployment.

It is intended to evolve as new technologies and application features are introduced.

## 2. Scope

This policy applies to the following project components:

| Component | Scope |
|---|---|
| Application | Python, FastAPI, and future frontend components |
| Dependencies | Python packages and third-party libraries |
| Containers | Docker images and Docker Compose |
| Database | PostgreSQL and future data persistence |
| Source Control | Git, GitHub, and pull requests |
| CI/CD | GitHub Actions, Pytest, Semgrep, and Trivy |
| Infrastructure | Future Kubernetes and Terraform configurations |
| User Data | Future authentication, profiles, availability, and scheduling information |

New components will be added to this table as the project expands.

## 3. Security Principles

DC Tennis Connect follows these principles:

- **Least Privilege:** Grant only the permissions necessary for each component.
- **Secure by Default:** Prefer secure configurations during initial implementation.
- **Defense in Depth:** Use multiple complementary security controls.
- **Automated Verification:** Test and scan changes consistently.
- **Minimal Exposure:** Limit unnecessary network access and runtime dependencies.
- **Traceability:** Document security findings, remediation decisions, and exceptions.
- **Continuous Improvement:** Reassess security controls as the application evolves.

## 4. Secure Development Requirements

All application and infrastructure changes should follow these practices:

1. Develop changes using dedicated Git feature branches.
2. Review changes through GitHub pull requests.
3. Do not commit credentials, tokens, or other secrets.
4. Validate external and user-provided input.
5. Apply appropriate authentication and authorization as features are introduced.
6. Maintain automated tests for implemented functionality.
7. Review relevant security scan results before merging.
8. Update affected architecture and security documentation.

## 5. Continuous Integration Security Controls

### 5.1 Current CI Controls

| Control | Technology | Current Enforcement |
|---|---|---|
| Automated application testing | Pytest | Test failures fail the job |
| Dependency consistency | pip | Dependency conflicts fail the job |
| Static application security testing | Semgrep | Configured `ERROR` findings fail the job |
| Container vulnerability scanning | Trivy | Findings reported; vulnerability gate deferred |
| Workflow permissions | GitHub Actions | Read-only repository access |
| Workflow execution | GitHub Actions | Timeouts and concurrency controls |

These controls represent the current Phase 4 implementation.

### 5.2 Planned CI Improvements

- Pin GitHub Actions dependencies to verified commit SHAs.
- Establish a consistent Trivy vulnerability baseline.
- Introduce risk-based vulnerability enforcement.
- Improve scan reporting and historical comparisons.
- Expand automated security checks for Kubernetes and Terraform.
- Reevaluate CI requirements as additional application features are introduced.

### 5.3 Branch Protection

GitHub branch protection is deferred during initial solo development.

The project currently relies on manual pull request review supported by automated CI checks.

Branch protection will be reconsidered before public deployment or when additional developers begin contributing.

## 6. Vulnerability Management

### 6.1 Severity and Prioritization

| Severity | Required Handling |
|---|---|
| Critical | Investigate promptly and prioritize remediation |
| High | Perform priority investigation and remediation planning |
| Medium | Document and prioritize based on exposure and impact |
| Low | Track through routine dependency and infrastructure maintenance |
| Unknown | Investigate where potential impact warrants additional review |

Severity alone does not establish exploitability.

Risk assessments should consider affected components, application exposure, available fixes, and potential impact.

### 6.2 Finding Status

| Status | Definition |
|---|---|
| Open | Finding identified but not yet assessed |
| Investigating | Applicability and security impact under review |
| Remediation Planned | Corrective action identified but not completed |
| Resolved | Remediation implemented and verified |
| Risk Accepted | Risk formally accepted with documented justification |
| False Positive | Finding determined not applicable based on supporting evidence |

### 6.3 Findings Register

Security findings, remediation history, scan results, and outstanding risks are maintained in:

`docs/runbooks/security-findings.md`

This policy defines security requirements. The findings register records actual security observations and decisions.

## 7. Security Exceptions and Risk Acceptance

Security exceptions must include:

| Field | Required Information |
|---|---|
| Finding ID | Unique identifier |
| Affected Component | Package, service, or configuration |
| Risk Description | Security concern and potential impact |
| Justification | Reason remediation is deferred |
| Compensating Controls | Measures reducing exposure |
| Responsible Reviewer | Person accountable for the decision |
| Review Date | Date for reassessment |
| Status | Current exception status |

Exceptions must be reviewed periodically and must not be used to conceal findings.

Risk acceptance does not mean the underlying vulnerability has been resolved.

## 8. Container and Infrastructure Security

### 8.1 Docker and Docker Compose

Containerized services should:

- Run as non-root users where practical.
- Minimize unnecessary runtime packages.
- Avoid embedding secrets in images.
- Use maintained base images.
- Limit published network ports.
- Separate application and database services.
- Preserve persistent data using appropriate storage.
- Undergo vulnerability scanning.

### 8.2 Planned Container Hardening

- Evaluate multi-stage Docker builds.
- Pin base images to verified digests.
- Review container filesystem permissions.
- Evaluate read-only filesystems and Linux capability restrictions.
- Review container image-layer risks.
- Introduce appropriate resource limits.

### 8.3 Kubernetes and Terraform

Security requirements for Kubernetes and Terraform will be defined as those technologies are introduced.

Planned areas include:

- Kubernetes RBAC.
- Pod and container security contexts.
- Network policies.
- Kubernetes Secret handling.
- Infrastructure configuration scanning.
- Terraform state protection.
- Least-privilege infrastructure permissions.

## 9. Secrets and Data Protection

### 9.1 Current Development Practices

- Credentials must not be committed to Git.
- Local environment files containing secrets must be excluded from version control.
- Application and database services should use the minimum required access.
- Sensitive values must not be unnecessarily exposed through logs or CI output.

### 9.2 Future Application Requirements

Before introducing real player information, the project must implement appropriate controls for:

- Authentication and authorization.
- Player profile information.
- Availability and scheduling details.
- Secure session handling.
- Protection of stored and transmitted data.
- Appropriate data retention and deletion.

## 10. GitHub Actions Security

GitHub Actions workflows should:

- Use least-privilege token permissions.
- Avoid unnecessary access to secrets.
- Use trusted and verified third-party actions.
- Apply reasonable execution timeouts.
- Prevent unnecessary overlapping runs.
- Fail when required tests or scanner execution fail.
- Pin external actions to verified commit SHAs as part of future hardening.

Workflow changes must be reviewed before merging.

## 11. Deployment Security Requirements

DC Tennis Connect is currently intended for local development.

Before public deployment, the project must review and implement appropriate controls for:

- Authentication and authorization.
- HTTPS and secure network access.
- Production secrets management.
- Database security.
- Outstanding vulnerability remediation.
- Logging and monitoring.
- Backup and recovery.
- Security testing and CI enforcement.
- User data protection.

A successful CI workflow does not automatically authorize production deployment.

## 12. Policy Maintenance and Change Management

### 12.1 When to Update This Policy

Review and update this policy when:

- A new technology is introduced.
- A significant application feature is implemented.
- Security architecture changes.
- CI/CD enforcement rules change.
- New data protection requirements arise.
- The application moves toward public deployment.

### 12.2 Change Management Process

1. Identify the affected policy section.
2. Update the relevant security requirements.
3. Review related architecture and findings documentation.
4. Commit the changes on a Git feature branch.
5. Review changes through a GitHub pull request.
6. Merge approved changes into `main`.

### 12.3 Policy Review History

| Date | Phase | Change | Status |
|---|---|---|---|
| 2026-10-26 | Phase 4 | Reorganized policy and documented current DevSecOps controls | Proposed |

Future policy changes should be added to this table.

---

## 13. Related Documentation

| Document | Purpose |
|---|---|
| `docs/runbooks/security-findings.md` | Security findings, scan results, remediation, and risk decisions |
| `docs/architecture/system-overview.md` | Application architecture and security design |
| `.github/workflows/security-ci.yml` | Automated testing and security scanning configuration |
| `docker/Dockerfile` | FastAPI container build configuration |
| `docker/compose.yaml` | Local application and database service configuration |

Additional security documentation can be referenced here as the project expands.