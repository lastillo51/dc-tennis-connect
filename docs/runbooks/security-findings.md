# DC Tennis Connect — Security Findings Register

> **Purpose:** Living record of security scans, investigations, remediation evidence, residual risks, and follow-up decisions.  
> **Current project stage:** Phase 6 — Terraform and Infrastructure as Code  
> **Latest dated scan in this register:** 2026-10-25 (Terraform scan date not yet recorded)  
> **Deployment status:** Local development only; not approved for public deployment.

## 1. Current Security Overview

Update this summary when new evidence is verified. Preserve historical results in Section 2 and the scan history in Section 7.

| Area | Recorded evidence | Assessment |
|---|---|---|
| Application tests | 16 Pytest tests passed | Passing at recorded verification |
| Dependency consistency | `python -m pip check` passed | Passing at recorded verification |
| Semgrep application scan | 0 findings on 2026-10-25 using `p/security-audit` | No findings under that scan's coverage |
| Trivy targeted image rescan | 0 High/Critical findings after packaging-tool removal | Must be reconciled with full image baseline |
| Trivy full image baseline | 164 findings, including 44 High | High findings remain outstanding for assessment |
| Trivy Terraform IaC scan | 0 findings recorded; date and scanner version missing | Reported zero; evidence metadata incomplete |
| GitHub Actions | Python, Semgrep, and container Trivy jobs reported successful | Existing CI operational; Terraform job not yet verified in this register |
| Post-remediation container runtime | No explicit evidence linked in this register | Evidence not yet recorded |
| Container image layers | Packaging tools uninstalled in a later layer | Residual exposure needs assessment |

**Do not combine scan results without matching the target image/configuration, scanner version, vulnerability database, scan date, and options.** In particular, the targeted zero-High result does not invalidate the 44-High full image baseline.

## 2. Security Scan Baselines

### 2.1 Trivy — Full Container Image Baseline

| Field | Recorded value |
|---|---|
| Scanner | Trivy 0.76.1 |
| Date | 2026-10-25 |
| Image | `dc-tennis-connect:dev` |
| Image ID | `sha256:364ca4eccae0b416dcd6ac2f10025acb9dd2f7554527ff07b7a2cdff96ca2d4a` |
| Scope | UNKNOWN, LOW, MEDIUM, HIGH, CRITICAL |
| Detailed report | `~/trivy-lab/trivy-results.json` (local only) |

| Severity | Findings |
|---|---:|
| Critical | 0 |
| High | 44 |
| Medium | 58 |
| Low | 61 |
| Unknown | 1 |
| **Total** | **164** |

These are scanner findings, not necessarily unique packages or confirmed exploitable vulnerabilities. This is **not** a clean security baseline.

### 2.2 Trivy — Targeted Container Image Scans

| Scan | High/Critical findings | Notes |
|---|---:|---|
| Before packaging-tool remediation | 4 | Four packaging-related advisories |
| After packaging-tool remediation | 0 | Previously reported advisories no longer detected |

**Open discrepancy:** Equivalent image identity, scan date, scanner/database versions, and flags have not been established for comparison with Section 2.1. The 44 High findings remain outstanding.

### 2.3 Semgrep — Application Source Baseline

| Field | Recorded value |
|---|---|
| Scanner | Semgrep CLI 1.182.1 |
| Date | 2026-10-25 |
| Target | `app/` |
| Ruleset | `p/security-audit` |
| Branch | `security/initial-scanning` |
| Detailed report | `~/semgrep-lab/semgrep-results.json` (local only) |

| Severity | Findings |
|---|---:|
| Error | 0 |
| Warning | 0 |
| Info | 0 |
| Unknown | 0 |
| **Total** | **0** |

No findings were reported under this ruleset at that time. This does not establish that the application has no security weaknesses.

### 2.4 Trivy — Terraform IaC Baseline (Phase 6)

| Field | Recorded value |
|---|---|
| Scanner | Trivy configuration scanner |
| Scan type | Infrastructure as Code / misconfiguration |
| Target | `terraform/` |
| Date | **Not recorded — add actual scan date** |
| Trivy version | **Not recorded — add installed version** |
| Branch | `infra/terraform-foundation` |
| Detailed report | `~/trivy-lab/terraform-config-results.json` (local only) |
| Command | `trivy config --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL terraform/` |

| Severity | Recorded findings |
|---|---:|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Unknown | 0 |
| **Total** | **0** |

The supplied document records zero Terraform misconfigurations. **Confirm the command completed successfully and fill in the scan date/version before treating this as a fully evidenced baseline.** Zero findings do not guarantee secure infrastructure, and the current configuration manages only local demonstration resources.

## 3. Individual Security Findings

Keep one row per actionable advisory or configuration issue. Preserve closed findings for traceability.

| ID | Component | Advisory | Detected version | Reported fix | Current status |
|---|---|---|---|---|---|
| SEC-001 | `msgpack` | GHSA-6v7p-g79w-8964 | 1.1.2 | 1.2.1 | Investigating — absent from targeted rescan |
| SEC-002 | `setuptools` | CVE-2025-47273 | 70.3.0 | 78.1.1 | Investigating — source unconfirmed |
| SEC-003 | `urllib3` | CVE-2026-97687 | 2.7.0 | 2.8.0 | Investigating — absent from targeted rescan |
| SEC-004 | `urllib3` | CVE-2026-97689 | 2.7.0 | 2.8.0 | Investigating — absent from targeted rescan |

### 3.1 Investigation and Remediation Evidence

- **Observed origin:** `msgpack` 1.1.2 and `urllib3` 2.7.0 were found bundled with `pip` 26.2.2 under `pip/_vendor`, rather than listed as separate packages by `pip list` or `importlib.metadata`.
- **Unconfirmed origin:** `setuptools` was not found in the searched runtime directories.
- **Change:** Dockerfile updated to uninstall Python packaging tools after installing application dependencies. Image rebuilt, exported, and rescanned.
- **Recorded checks:** Targeted High/Critical rescan reported zero; 16 Pytest tests passed; `python -m pip check` reported no broken requirements.
- **Residual risk:** Files from removed packaging tools may remain in earlier image layers. Evaluate a multi-stage build and rescan the distributed image.

Do not mark SEC-001 through SEC-004 fully resolved until the image-baseline discrepancy and remaining exposure are investigated or explicitly assessed and accepted.

### 3.2 Finding Status Definitions

| Status | Meaning |
|---|---|
| Open | Identified; assessment pending |
| Investigating | Origin, applicability, or exposure being evaluated |
| Remediation Planned | Corrective action identified but not complete |
| Resolved | Remediation implemented and verified with evidence |
| Risk Accepted | Documented acceptance with rationale, reviewer, and review date |
| False Positive | Evidence demonstrates that the finding does not apply |

## 4. GitHub Actions Security CI

### 4.1 Recorded Phase 4 Baseline

| Field | Recorded value |
|---|---|
| Workflow | DC Tennis Connect Security CI |
| File | `.github/workflows/security-ci.yml` |
| Branch at initial successful run | `security/initial-scanning` |
| Initial successful execution date | 2026-10-25 |
| Workflow page | https://github.com/lastillo51/dc-tennis-connect/actions/workflows/security-ci.yml |
| Recorded commit | `c602d7734ad14c4bf737aadd02ce64e1110b4d63` |
| Specific successful run URL | Not recorded |

The workflow page is not an individual run. The commit has not been independently matched to a specific run in this register.

| Check | Recorded result | Enforcement |
|---|---|---|
| Pytest | Passed | Test failures fail job |
| Dependency consistency | Passed | `pip check` failures fail job |
| Semgrep | Passed | Configured `ERROR` findings fail job |
| Trivy container image | Passed | Findings report-only; scanner execution failures should fail job |

Implemented controls include separate jobs, push/PR checks, read-only repository token permissions, job timeouts, concurrency controls, and image builds on GitHub-hosted runners.

### 4.2 Phase 6 Terraform CI — Planned / Pending Verification

| Check | Intended enforcement | Verification status |
|---|---|---|
| Terraform formatting | Fail on formatting errors | Pending CI evidence |
| Terraform initialization | Fail on initialization errors | Pending CI evidence |
| Terraform validation | Fail on invalid configuration | Pending CI evidence |
| Trivy IaC scan | Report misconfigurations; scanner errors fail job | Pending CI evidence |

After the Terraform CI job runs, record its run URL, commit SHA, tool versions, outcome, and any differences from the local IaC scan. Do not mark this job implemented and verified solely because it is described here.

### 4.3 CI Limitations

- Passing security jobs does not prove the absence of vulnerabilities.
- Scanner results may vary by tool version, rules, databases, and target contents.
- GitHub Actions dependencies are not yet documented as pinned to verified commit SHAs.
- Branch protection is deferred for solo development; PR checks are reviewed manually.
- Trivy vulnerability and IaC misconfiguration findings are currently planned to remain report-only until risk-based gates are defined.

## 5. Risk Decisions and Prioritization

| Severity | Handling |
|---|---|
| Critical | Investigate promptly; assess blocking work or deployment |
| High | Prioritize exposure, applicability, and available fixes |
| Medium | Track and schedule remediation; escalate exposed issues |
| Low | Review during routine maintenance |
| Unknown | Investigate context and classify where possible |

**Current decisions:** Continue local development, but do not approve public deployment based on current evidence. Keep container-image Trivy findings report-only until the baseline is reconciled. Treat 44 High findings as outstanding for triage. Defer branch protection while manually reviewing CI results.

Deferral is **not** remediation or formal risk acceptance. A formal exception must identify the finding, justification, compensating controls, accountable reviewer, and reassessment date.

## 6. Open Actions Tracker

| ID | Action | Priority | Status | Completion evidence |
|---|---|---|---|---|
| ACT-001 | Reconcile targeted and full Trivy image scans | High | Open | Compare image IDs, dates, versions, databases, flags |
| ACT-002 | Triage 44 High image findings | High | Open | Record applicability, fixes, and decisions |
| ACT-003 | Link post-remediation runtime verification | Medium | Evidence pending | Startup, non-root execution, health/court endpoints |
| ACT-004 | Evaluate multi-stage runtime image | Medium | Planned | Rebuild, rescan, assess image layers |
| ACT-005 | Record exact successful Phase 4 CI run | Low | Open | Run URL and associated commit |
| ACT-006 | Pin GitHub Actions dependencies | Medium | Planned | Verified full commit SHA references |
| ACT-007 | Establish risk-based container Trivy gate | Medium | Deferred | Reviewed baseline and enforcement policy |
| ACT-008 | Review Medium, Low, and Unknown image findings | Routine | Planned | Scheduled reassessment |
| ACT-009 | Complete Terraform IaC scan metadata | Low | Open | Actual date, version, successful scan evidence |
| ACT-010 | Verify Terraform CI job | Medium | Pending | Run URL, commit, formatting/validation/scan results |
| ACT-011 | Define IaC misconfiguration enforcement | Medium | Planned | Risk-based policy and thresholds |
| ACT-012 | Expand IaC controls for cloud deployment | Future | Planned | Cloud-specific security review and scan evidence |

## 7. Scan History and Repeatable Workflow

### 7.1 Scan History

Append new rows; do not overwrite older results. A dash means not applicable or not recorded, **not zero**.

| Date | Scanner / scope | Target | Critical | High | Medium | Low | Unknown | Notes |
|---|---|---|---:|---:|---:|---:|---:|---|
| 2026-10-25 | Trivy image, full severity | `dc-tennis-connect:dev` | 0 | 44 | 58 | 61 | 1 | Image ID and report in §2.1 |
| Not recorded | Trivy image, targeted pre-remediation | Image not recorded | — | — | — | — | — | 4 combined High/Critical |
| Not recorded | Trivy image, targeted post-remediation | Image not recorded | — | — | — | — | — | 0 combined High/Critical |
| 2026-10-25 | Semgrep `p/security-audit` | `app/` | — | — | — | — | — | 0 total findings; §2.3 |
| Not recorded | Trivy Terraform IaC | `terraform/` | 0 | 0 | 0 | 0 | 0 | Reported 0; metadata incomplete; §2.4 |

### 7.2 Procedure for Future Scans

1. Record date, branch/commit, target image ID or IaC path, scanner version, rule/database information, and exact command.
2. Save detailed reports outside Git unless sanitized and explicitly approved for inclusion.
3. Append a new history entry without deleting older observations.
4. Update the current overview only after checking scan comparability.
5. Add or update individual findings and remediation evidence.
6. Record regression tests and runtime verification after changes.
7. Update open actions and review the Markdown diff before committing.

### 7.3 New Finding Template

Copy and complete this template for each new actionable issue:

```markdown
#### SEC-XXX — Finding title

- **Scanner / advisory:**
- **Component and version:**
- **First detected:**
- **Severity / exposure:**
- **Evidence / report:**
- **Status:** Open
- **Owner / reviewer:**
- **Remediation or risk decision:**
- **Verification:**
- **Next review date:**
```

## 8. Repository Handling and Review Triggers

This Markdown register is intended for Git. Keep raw scanner JSON, Docker image archives, local `.env` files, Terraform state, private `.tfvars` values, credentials, and other sensitive artifacts outside the repository. Review staged changes before committing.

**Review this register after:** A new Trivy or Semgrep scan; dependency, base-image, or Terraform change; CI policy change; completion of an open action; or preparation for cloud deployment.

**Project context:** DC Tennis Connect runs locally, uses fictional court data, and does not currently store production player information. This limits current external exposure but does not eliminate development-environment risk or future deployment obligations.