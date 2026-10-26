# DC Tennis Connect — Security Findings Register

> **Document purpose:** Living record of security scan results, finding investigations, remediation evidence, residual risks, and follow-up decisions.  
> **Project stage:** Phase 4 — Security scanning and CI/CD  
> **Last recorded scan date:** 2026-10-25  
> **Status:** Local development only; not approved for public deployment.

## 1. Current Security Overview

This section is the starting point for each review. Update it when new evidence changes the project's security status; retain older scan results in the history below.

| Area | Latest documented evidence | Current assessment |
|---|---|---|
| Automated application tests | 16 Pytest tests passed | Passing in recorded verification |
| Dependency consistency | `python -m pip check` passed | Passing in recorded verification |
| Semgrep | 0 findings with `p/security-audit` on 2026-10-25 | No findings in that scan; coverage is limited |
| Trivy targeted High/Critical rescan | 0 findings reported after packaging-tool removal | Result recorded; requires comparison with full baseline |
| Trivy full-severity baseline | 164 findings, including 44 High | High findings remain outstanding for assessment |
| GitHub Actions | Pytest, Semgrep, and Trivy jobs reported successful | CI operational; scanner success does not imply zero vulnerabilities |
| Post-remediation container runtime test | No explicit verification evidence in this register | Verification not yet recorded |
| Docker image-layer exposure | Packaging tools removed in a later image layer | Residual risk remains under investigation |

**Interpretation:** The zero-High targeted result and the 44-High full baseline are separate observations. The supplied record does not establish that they used the same image, database snapshot, or scan configuration. Do not describe the full image as free of High vulnerabilities.

## 2. Scan Inventory and Results

### 2.1 Trivy — Full Image Baseline

| Attribute | Recorded value |
|---|---|
| Scanner | Trivy 0.76.1 |
| Scan date | 2026-10-25 |
| Target | `dc-tennis-connect:dev` |
| Image ID | `sha256:364ca4eccae0b416dcd6ac2f10025acb9dd2f7554527ff07b7a2cdff96ca2d4a` |
| Severity scope | UNKNOWN, LOW, MEDIUM, HIGH, CRITICAL |
| Detailed report | `~/trivy-lab/trivy-results.json` — local only, not committed |

| Severity | Findings |
|---|---:|
| Critical | 0 |
| High | 44 |
| Medium | 58 |
| Low | 61 |
| Unknown | 1 |
| **Total** | **164** |

These are scanner-reported findings, not necessarily unique packages or confirmed exploitable vulnerabilities. This baseline is **not** a clean security result.

### 2.2 Trivy — Targeted High/Critical Scans

| Scan | Reported High/Critical findings | Notes |
|---|---:|---|
| Initial targeted scan | 4 | Four Python packaging-related advisories identified |
| Post-remediation targeted scan | 0 | Findings no longer reported after Dockerfile change |

**Open reconciliation:** The scan records do not yet establish equivalent image IDs, Trivy databases, dates, and settings. Treat the 44 High findings in the full baseline as outstanding until investigated.

### 2.3 Semgrep — Python Source Scan

| Attribute | Recorded value |
|---|---|
| Scanner | Semgrep CLI 1.182.1 |
| Scan date | 2026-10-25 |
| Target | `app/` |
| Ruleset | `p/security-audit` |
| Branch | `security/initial-scanning` |
| Detailed report | `~/semgrep-lab/semgrep-results.json` — local only, not committed |

| Severity | Findings |
|---|---:|
| Error | 0 |
| Warning | 0 |
| Info | 0 |
| Unknown | 0 |
| **Total** | **0** |

No findings were reported by this ruleset on this scan. This does not guarantee that the application is free of security weaknesses, including authorization or business-logic flaws.

## 3. Individual Finding Register

Use one row per actionable advisory or configuration issue. Keep historical findings even after remediation, with evidence supporting status changes.

| ID | Component | Advisory | Detected version | Reported fix | Status |
|---|---|---|---|---|---|
| SEC-001 | `msgpack` | GHSA-6v7p-g79w-8964 | 1.1.2 | 1.2.1 | Investigating — absent in targeted rescan |
| SEC-002 | `setuptools` | CVE-2025-47273 | 70.3.0 | 78.1.1 | Investigating — source not confirmed |
| SEC-003 | `urllib3` | CVE-2026-97687 | 2.7.0 | 2.8.0 | Investigating — absent in targeted rescan |
| SEC-004 | `urllib3` | CVE-2026-97689 | 2.7.0 | 2.8.0 | Investigating — absent in targeted rescan |

### 3.1 Investigation and Remediation History

**Observed origin:** `msgpack` 1.1.2 and `urllib3` 2.7.0 were found in `pip` 26.2.2 under `pip/_vendor`. They were not independently listed by `pip list` or `importlib.metadata`. `setuptools` was not found in the searched runtime directories; its detection source remains unconfirmed.

**Change made:** The Dockerfile was updated to uninstall Python packaging tools after dependency installation. The image was rebuilt, exported, and rescanned.

**Recorded verification:** The targeted High/Critical rescan no longer reported SEC-001 through SEC-004; 16 Pytest tests passed, and `python -m pip check` reported no broken requirements. A post-remediation container runtime test is not explicitly recorded in the supplied document.

**Residual risk:** Removing packaging tools in a later Docker layer can leave their bytes in earlier layers. Evaluate a multi-stage build with a minimal runtime stage, then rebuild and rescan. Do not mark SEC-001 through SEC-004 fully resolved until the full-baseline discrepancy and residual risk are addressed or explicitly assessed and accepted.

### 3.2 Finding Status Definitions

| Status | Meaning |
|---|---|
| Open | Detected; initial assessment pending |
| Investigating | Applicability, exposure, or origin being evaluated |
| Remediation Planned | Fix identified but not yet applied |
| Resolved | Fix implemented and verified with evidence |
| Risk Accepted | Residual risk accepted with rationale, reviewer, and review date |
| False Positive | Evidence shows finding does not apply |

## 4. GitHub Actions CI Baseline

| Attribute | Recorded value |
|---|---|
| Workflow | DC Tennis Connect Security CI |
| Workflow file | `.github/workflows/security-ci.yml` |
| Branch at initial successful run | `security/initial-scanning` |
| Initial successful execution date | 2026-10-25 |
| Workflow page | https://github.com/lastillo51/dc-tennis-connect/actions/workflows/security-ci.yml |
| Recorded commit SHA | `c602d7734ad14c4bf737aadd02ce64e1110b4d63` |
| Specific successful run URL | Not recorded; add the individual run URL when available |

The workflow-page URL above identifies the workflow, **not a particular run**. The recorded commit SHA has not been independently matched to a run in this document.

| Check | Recorded execution | Enforcement as documented |
|---|---|---|
| Pytest | Passed | Test failures fail the job |
| Dependency consistency | Passed | `pip check` failures fail the job |
| Semgrep | Passed | `ERROR` findings configured to fail the scan job in the hardened workflow |
| Trivy | Passed | Vulnerability findings report-only; execution failures should fail the job |

**Controls implemented:** Separate CI jobs; automated push and pull-request checks; read-only repository token permissions; Docker image build on GitHub-hosted runner; Trivy installation through the Ubuntu package repository; and documented workflow timeouts and concurrency controls.

**Limitations:** Scanner results may vary with tool versions, rules, vulnerability databases, and image contents. A successful CI run does not demonstrate zero vulnerabilities. GitHub Actions references are not yet documented as pinned to verified commit SHAs. Branch protection is deferred for this solo development project.

## 5. Risk Decisions and Prioritization

| Severity | Current handling |
|---|---|
| Critical | Investigate promptly; assess whether work or deployment should be blocked |
| High | Prioritize applicability, exposure, and available fixes; do not silently accept |
| Medium | Track and schedule remediation; escalate exposed or actively exploited issues |
| Low | Review during routine dependency and image maintenance |
| Unknown | Investigate advisory context and classify where possible |

**Current decisions:**

- Continue local development and DevSecOps learning; the application is not approved for public deployment.
- Keep Trivy vulnerability findings report-only in CI until the baseline is reconciled and a risk-based enforcement policy is established.
- Treat the recorded 44 High findings as outstanding and untriaged for planning purposes.
- Defer branch protection for now; review CI checks manually before merging.
- Do not interpret a zero-finding Semgrep scan or successful Trivy job as proof of complete security.

Deferral is not remediation or formal risk acceptance. Any risk acceptance must record the affected finding, rationale, compensating controls, accountable reviewer, and reassessment date.

## 6. Open Actions Tracker

Update this table as work progresses. Use a GitHub issue or pull request link when one is created.

| ID | Action | Priority | Status | Evidence / completion condition |
|---|---|---|---|---|
| ACT-001 | Reconcile targeted and full Trivy results | High | Open | Compare image ID, scan time, Trivy version, database, and flags |
| ACT-002 | Triage 44 High findings from full baseline | High | Open | Record applicability, available fixes, and decisions |
| ACT-003 | Verify post-remediation container runtime | Medium | Evidence pending | Confirm startup, non-root user, health and court endpoints |
| ACT-004 | Evaluate multi-stage runtime image | Medium | Planned | Rebuild and rescan; document image-layer exposure |
| ACT-005 | Capture exact successful GitHub Actions run URL | Low | Open | Link to run and associated commit |
| ACT-006 | Review and pin GitHub Actions dependencies | Medium | Planned | Verified full commit SHA references |
| ACT-007 | Establish risk-based Trivy merge gate | Medium | Deferred | Approved baseline and enforcement criteria |
| ACT-008 | Review Medium, Low, and Unknown findings | Routine | Planned | Reassessment during dependency maintenance |

## 7. Repeatable Process for Future Scans

1. Record the date, Git commit, image ID or digest, scanner version, ruleset/database information, and command used.
2. Save detailed machine-readable reports outside Git unless sanitized and intentionally approved for inclusion.
3. Add a new scan entry to the history table below; **do not overwrite earlier results**.
4. Update the current overview and counts only after identifying which scan is authoritative for the intended target.
5. Create or update individual finding rows for issues requiring investigation, remediation, or acceptance.
6. Run appropriate application and container verification after changes; record evidence.
7. Update the actions tracker, then review the Markdown diff before committing.

### 7.1 Scan History

| Date | Scanner / scope | Target or commit | Critical | High | Medium | Low | Unknown | Evidence / notes |
|---|---|---|---:|---:|---:|---:|---:|---|
| 2026-10-25 | Trivy full severity | `dc-tennis-connect:dev` (image ID in §2.1) | 0 | 44 | 58 | 61 | 1 | Local JSON report |
| Not recorded | Trivy targeted before remediation | Image identity not recorded | Not separated | 4 combined High/Critical | — | — | — | Initial targeted scan |
| Not recorded | Trivy targeted after remediation | Image identity not recorded | 0 combined | 0 combined | — | — | — | Targeted rescan; requires reconciliation |
| 2026-10-25 | Semgrep `p/security-audit` | `app/` | — | — | — | — | — | 0 total findings; see §2.3 |

For new scans, append a row with actual counts and a reference to the corresponding local report. Use `—` when a severity was not scanned or is not applicable; do not substitute zero for unknown values.

### 7.2 New Finding Template

Copy this subsection for an issue requiring individual tracking:

```markdown
#### SEC-XXX — Short finding title

- **Scanner / advisory:**
- **Component and version:**
- **First detected:**
- **Severity / exposure:**
- **Evidence:**
- **Status:** Open
- **Owner / reviewer:**
- **Remediation or decision:**
- **Verification:**
- **Next review date:**
```

## 8. Repository Handling and Next Review

This Markdown register is intended for Git. Keep raw scanner JSON, Docker image archives, local `.env` files, credentials, and other sensitive artifacts outside the repository. Review staged changes before committing.

**Next review trigger:** New Trivy or Semgrep scan; dependency or base-image change; CI policy change; or completion of an open action above.

**Project context:** DC Tennis Connect currently runs locally, uses fictional court data, and does not store production player information. That limits current external exposure but does not eliminate development-environment risk or future deployment obligations.