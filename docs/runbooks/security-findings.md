# DC Tennis Connect — Security Findings Register

## 1. Purpose and Scope

This document records the security scanning baseline, investigations, remediation attempts, residual risks, and follow-up decisions for DC Tennis Connect during Phase 4. It covers the local FastAPI Docker image and static analysis of the Python application.

Findings are tracked separately from their remediation status. A clean targeted scan does not establish that the entire image is vulnerability-free, and a scanner finding is not by itself proof of exploitability.

## 2. Trivy — Initial Findings and Remediation

### Initial High-Severity Findings

The initial targeted Trivy scan reported four High-severity Python package vulnerabilities:

| ID | Package | Advisory | Detected version | Reported fixed version |
|---|---|---|---|---|
| SEC-001 | `msgpack` | GHSA-6v7p-g79w-8964 | 1.1.2 | 1.2.1 |
| SEC-002 | `setuptools` | CVE-2025-47273 | 70.3.0 | 78.1.1 |
| SEC-003 | `urllib3` | CVE-2026-97687 | 2.7.0 | 2.8.0 |
| SEC-004 | `urllib3` | CVE-2026-97689 | 2.7.0 | 2.8.0 |

### Root Cause Investigation

Inspection confirmed that `msgpack` 1.1.2 and `urllib3` 2.7.0 were bundled within `pip` 26.2.2 (`pip/_vendor`) in the container. Neither appeared as an independently installed distribution in `pip list` or `importlib.metadata`.

`setuptools` was not found in the runtime directories searched. Its original detection source has not been conclusively established.

### Remediation Performed

The Dockerfile was modified to uninstall Python packaging tools after installing application dependencies. The image was rebuilt, exported, and rescanned.

### Targeted Scan Verification

| Check | Recorded result |
|---|---|
| Initial targeted High/Critical scan | 4 findings |
| Subsequent targeted High/Critical scan | 0 findings reported |
| Local Pytest suite | 16 tests passed |
| Local `python -m pip check` | No broken requirements found |
| Containerized application runtime after remediation | Not yet recorded as verified |

The targeted rescan no longer reported SEC-001 through SEC-004. **This does not mean that all High-severity findings are resolved:** the separately recorded full-severity scan reports 44 High findings. The differing results require reconciliation by image identity, scan timestamp, scanner database, and scan configuration.

### Residual Image-Layer Risk

Uninstalling packages in a later Docker layer can leave their bytes in earlier layers of the distributed image. A multi-stage build with a minimal runtime stage should be evaluated. A clean scanner result does not demonstrate that these earlier-layer bytes are absent.

**SEC-001–SEC-004 status:** No longer reported in the targeted rescan; pending reconciliation with the full baseline and closure of residual image-layer risk. Do not classify as fully resolved yet.

## 3. Trivy — Full Vulnerability Baseline

### Scan Information

| Attribute | Recorded value |
|---|---|
| Scanner | Trivy 0.76.1 |
| Target | DC Tennis Connect Docker image |
| Image tag | `dc-tennis-connect:dev` |
| Recorded image ID | `sha256:364ca4eccae0b416dcd6ac2f10025acb9dd2f7554527ff07b7a2cdff96ca2d4a` |
| Scan date | 2026-10-25 |
| Severity scope | UNKNOWN, LOW, MEDIUM, HIGH, CRITICAL |
| Detailed report | `~/trivy-lab/trivy-results.json` (local-only; not committed) |

### Vulnerability Summary

| Severity | Findings |
|---|---:|
| Critical | 0 |
| High | 44 |
| Medium | 58 |
| Low | 61 |
| Unknown | 1 |
| **Total** | **164** |

These counts are preserved from the reported full scan. They are **not** a clean baseline. Counts represent scanner-reported findings, not necessarily unique vulnerable packages or confirmed exploitable issues.

### Reconciliation Required

The targeted post-remediation scan reported zero High/Critical findings, whereas the full-severity baseline records 44 High findings. Before using these counts to approve a merge or close issues, confirm:

1. Both reports scanned the same image ID and image archive.
2. Both scans used the same Trivy version, vulnerability database snapshot, and scanner settings.
3. The full report was generated **after** the intended Dockerfile remediation and image export.
4. Any differences caused by scanner data updates or scan timing are documented.
5. Outstanding High findings are reviewed and triaged, even if remediation is deferred.

Until reconciled, treat the **44 High findings as outstanding and untriaged** for planning purposes. Do not claim that the full image is free of High vulnerabilities.

### Prioritization and Handling

| Severity | Phase 4 handling |
|---|---|
| Critical | Investigate immediately; assess whether work or deployment should be blocked. |
| High | Prioritize triage, applicability, fix availability, and exposure; do not silently accept. |
| Medium | Track and schedule remediation; escalate exposed or actively exploited issues. |
| Low | Track for regular maintenance and image/dependency updates. |
| Unknown | Review advisory context and classify where possible. |

Any deferral or risk acceptance must identify the affected component, rationale, owner, and planned review date. Deferral is not equivalent to remediation.

### Current Exposure and Limitations

DC Tennis Connect is currently a local development application, not a public production service. Court records are fictional and production user information is not stored. This limits current external exposure but does not eliminate risks to the development environment or future deployments.

The detailed JSON report remains outside Git. Its path is a local reference, not a repository artifact; another developer must generate their own report.

### Follow-Up Actions

- Reconcile the targeted and full Trivy results before closing SEC-001–SEC-004.
- Triage the 44 reported High findings and document actionable or accepted items.
- Verify the rebuilt application container still starts, runs as non-root, and serves expected endpoints.
- Evaluate a multi-stage Dockerfile and rescan the resulting image.
- Recheck Medium, Low, and Unknown findings during routine dependency maintenance.
- Repeat scans after base-image or dependency changes and update this baseline.

**Current decision:** Continue local learning and documentation, but do not treat the image as security-cleared or ready for public deployment. Security-gate enforcement criteria will be defined in a later Phase 4 exercise.

## 4. Semgrep — Static Application Security Testing

### Scan Information

| Attribute | Recorded value |
|---|---|
| Scanner | Semgrep CLI 1.182.1 |
| Scan target | `app/` |
| Ruleset | `p/security-audit` |
| Scan date | 2026-10-25 |
| Git branch | `security/initial-scanning` |
| Detailed report | `~/semgrep-lab/semgrep-results.json` (local-only; not committed) |

### Findings Summary

| Severity | Findings |
|---|---:|
| Error | 0 |
| Warning | 0 |
| Info | 0 |
| Unknown | 0 |
| **Total** | **0** |

The selected ruleset reported no findings in the scanned application files. This is **not** proof that the application has no security weaknesses; detection depends on the ruleset, scanned files, and tool behavior.

### Findings Requiring Action

No findings were reported by the recorded Semgrep scan. No Semgrep-specific remediation is currently identified from this result.

### Future Finding Workflow

1. Review the rule ID, file, line, and reported code pattern.
2. Assess applicability, untrusted-input reachability, and security impact.
3. Record a finding when investigation, remediation, or risk acceptance is required.
4. Apply a targeted fix on a feature branch and rerun relevant tests.
5. Rescan and document the result before marking the issue resolved.

Use statuses: **Open**, **Investigating**, **Remediation Planned**, **Resolved**, **Risk Accepted**, or **False Positive**. Risk acceptance and false-positive decisions require supporting evidence.

### Limitations and Follow-Up

- Static analysis cannot guarantee complete security coverage.
- The public ruleset may miss application-specific authorization and business-logic flaws.
- Authentication, player matching, and scheduling have not yet been implemented.
- Introduce Semgrep into GitHub Actions in Phase 4, Exercise 4.
- Establish reviewed rule selection and failure thresholds before enabling blocking checks.
- Rerun Semgrep when security-sensitive application code changes.

## 5. Phase 4 Verification and Repository Readiness

| Item | Status |
|---|---|
| Trivy findings and scan counts documented | Complete |
| Semgrep scan results documented | Complete |
| Local Pytest suite | 16 passing (recorded) |
| Local dependency consistency | Passed (recorded) |
| Post-remediation container runtime verification | Pending evidence |
| Targeted versus full Trivy scan reconciliation | Pending |
| High-severity Trivy finding triage | Pending |
| Security automation in GitHub Actions | Planned for Exercise 4 |

### Repository Handling

This Markdown register is intended to be version-controlled. Raw scanner reports, local environment files, credentials, and image archives remain outside the repository. Review staged changes for secrets and unexpected artifacts before committing.

### Next Review

Update this register after reconciling Trivy scan results, validating the post-remediation container, and implementing the initial GitHub Actions security workflow.