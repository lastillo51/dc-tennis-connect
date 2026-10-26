# DC Tennis Connect — DevSecOps Security Policy

## 1. Purpose

Define security expectations for application development, dependency management, containerization, automated testing, vulnerability assessment, and deployment.

This policy will evolve as DC Tennis Connect introduces additional functionality.

## 2. Scope

This policy applies to:

- Python and FastAPI application code.
- Python dependencies.
- Docker images and Docker Compose.
- GitHub repositories and workflows.
- PostgreSQL configuration.
- Future Kubernetes and Terraform infrastructure.
- Future authentication, scheduling, and player information.

## 3. Development Security Requirements

- Develop changes using dedicated Git feature branches.
- Review changes through pull requests.
- Do not commit credentials or secrets.
- Validate application inputs.
- Apply least-privilege access controls.
- Maintain automated regression tests.
- Review security findings before merging significant changes.
- Keep security documentation updated.

## 4. CI Security Controls

### Pytest

Automated application tests must pass.

Test failures block the CI job.

### Dependency Consistency

`python -m pip check` must complete successfully.

### Semgrep

Semgrep analyzes application source code using approved rulesets.

Findings classified as `ERROR` by the configured rules will fail the Semgrep CI job.

Other findings will be assessed through broader scans and security reviews.

### Trivy

Trivy scans container images for known vulnerabilities.

During the initial CI implementation, vulnerabilities are reported without automatically failing the job.

Critical and High findings must be reviewed and documented.

Automatic vulnerability enforcement will be introduced after establishing a consistent, reviewed baseline.

### Branch Protection

GitHub branch protection is deferred during initial development.

The project currently uses a manual pull request review process,
supported by automated Pytest, Semgrep, and Trivy checks.

Branch protection will be reconsidered before public deployment
or when additional developers begin contributing.

## 5. Vulnerability Prioritization

| Severity | Required Handling |
|---|---|
| Critical | Prompt investigation and remediation planning |
| High | Priority investigation and remediation planning |
| Medium | Document and prioritize based on exposure |
| Low | Track through routine maintenance |
| Unknown | Investigate where potential impact warrants it |

Severity alone does not determine exploitability.

Assess affected components, exposure, available fixes, and potential impact.

## 6. Security Finding Status

Findings may be classified as:

- Open
- Investigating
- Remediation Planned
- Resolved
- Risk Accepted
- False Positive

Risk acceptance requires documented justification, an accountable reviewer, and a future reassessment date.

## 7. Security Exceptions

A security exception must record:

- Finding identifier.
- Affected component.
- Reason remediation is deferred.
- Risk assessment.
- Compensating controls.
- Responsible reviewer.
- Review or expiration date.

Exceptions must not be used simply to conceal scanner findings.

## 8. Container Security

Containerized applications should:

- Run as non-root users.
- Avoid unnecessary runtime dependencies.
- Exclude secrets from container images.
- Use maintained base images.
- Minimize exposed ports.
- Separate application and database services.
- Preserve necessary persistent data.
- Be scanned before deployment.

Image digest pinning and stronger runtime hardening will be introduced incrementally.

## 9. GitHub Actions Security

Workflows should:

- Use least-privilege permissions.
- Avoid unnecessary access to secrets.
- Apply reasonable execution timeouts.
- Prevent unnecessary overlapping runs.
- Use trusted and verified third-party actions.
- Pin actions to verified commit SHAs when practical.
- Fail when required tests or scanner execution fail.

## 10. Deployment Security

The current application is intended for local development.

Before public deployment, the project must evaluate:

- Authentication and authorization.
- HTTPS and secure network exposure.
- Secret management.
- Database access controls.
- Vulnerability remediation.
- Logging and monitoring.
- Backup and recovery.
- Required CI security checks.

## 11. Policy Maintenance

This document will be updated when significant security requirements or architectural decisions change.

Security policy changes must be version-controlled and reviewed through GitHub pull requests.