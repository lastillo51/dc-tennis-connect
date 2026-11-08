# DC Tennis Connect — Security Findings Register

> **Purpose:** Living record of security scans, investigations, remediation evidence, residual risks, and follow-up decisions.  
> **Current project stage:** Phase 7 — Frontend Development  
> **Latest fully dated historical scan:** 2026-10-25 (Phase 7 Semgrep and Terraform scan metadata pending)  
> **Deployment status:** Local development only; not approved for public deployment.

## 1. Current Security Overview

Update this summary when new evidence is verified. Preserve historical results in Section 2 and the scan history in Section 7.

| Area | Recorded evidence | Assessment |
|---|---|---|
| Application tests | 42 Pytest tests passed at the last reported Phase 7 checkpoint; one dependency deprecation warning | Final Step 11H suite results pending |
| Dependency consistency | `python -m pip check` passed | Passing at recorded verification |
| Semgrep application scan | 0 findings on 2026-10-25; 1 blocking template-URL finding during Phase 7 | New finding `SEC-FE-001` under investigation; historical baseline retained |
| Trivy targeted image rescan | 0 High/Critical findings after packaging-tool removal | Must be reconciled with full image baseline |
| Trivy full image baseline | 164 findings, including 44 High | High findings remain outstanding for assessment |
| Trivy Terraform IaC scan | 0 findings recorded; date and scanner version missing | Reported zero; evidence metadata incomplete |
| GitHub Actions | Four jobs reported passing during Phase 6, including Terraform IaC | Run URL, commit, and tool versions still need recording; Phase 7 finding not yet verified in CI |
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

### 2.5 Semgrep — Phase 7 Frontend Scan (Exercise 4)

| Field | Recorded value |
|---|---|
| Scanner | Semgrep CLI; exact version not recorded for this scan |
| Date | Not recorded — enter actual scan date |
| Target | `app/` |
| Ruleset | `p/security-audit` |
| Branch | `feature/frontend-foundation` (reported development branch) |
| Command | `semgrep scan --config p/security-audit app/` |
| Result | 1 code finding, labeled **Blocking** by Semgrep |
| Rule | `generic.html-templates.security.var-in-href.var-in-href` |
| Location | `app/templates/courts/detail.html:82` at time of scan |
| Detailed report | Terminal output; JSON report not recorded |

The rule flags the dynamic Jinja2 attribute `href="{{ google_maps_url }}"` as a potential XSS vector. **Blocking** is the scanner's reported designation; no independent numeric severity or exploitability rating has been established. This is a *new scan*, not a revision to the 2026-10-25 zero-finding baseline in §2.3.

**Current disposition:** Investigating; likely false positive **if** the frontend obtains the URL exclusively from `build_google_maps_url(court.location)` and that function always constructs a fixed HTTPS Google Maps URL. Verification and a documented decision are still required.

## 3. Individual Security Findings

Keep one row per actionable advisory or configuration issue. Preserve closed findings for traceability.

| ID | Component | Advisory | Detected version | Reported fix | Current status |
|---|---|---|---|---|---|
| SEC-001 | `msgpack` | GHSA-6v7p-g79w-8964 | 1.1.2 | 1.2.1 | Investigating — absent from targeted rescan |
| SEC-002 | `setuptools` | CVE-2025-47273 | 70.3.0 | 78.1.1 | Investigating — source unconfirmed |
| SEC-003 | `urllib3` | CVE-2026-97687 | 2.7.0 | 2.8.0 | Investigating — absent from targeted rescan |
| SEC-004 | `urllib3` | CVE-2026-97689 | 2.7.0 | 2.8.0 | Investigating — absent from targeted rescan |

### 3.1 Packaging Dependency Investigation and Remediation Evidence

- **Observed origin:** `msgpack` 1.1.2 and `urllib3` 2.7.0 were found bundled with `pip` 26.2.2 under `pip/_vendor`, rather than listed as separate packages by `pip list` or `importlib.metadata`.
- **Unconfirmed origin:** `setuptools` was not found in the searched runtime directories.
- **Change:** Dockerfile updated to uninstall Python packaging tools after installing application dependencies. Image rebuilt, exported, and rescanned.
- **Recorded checks:** Targeted High/Critical rescan reported zero; 16 Pytest tests passed; `python -m pip check` reported no broken requirements.
- **Residual risk:** Files from removed packaging tools may remain in earlier image layers. Evaluate a multi-stage build and rescan the distributed image.

Do not mark SEC-001 through SEC-004 fully resolved until the image-baseline discrepancy and remaining exposure are investigated or explicitly assessed and accepted.

### 3.2 SEC-FE-001 — Dynamic Google Maps URL in Jinja2 `href`

| Field | Value |
|---|---|
| Finding ID | `SEC-FE-001` |
| Scanner / rule | Semgrep — `generic.html-templates.security.var-in-href.var-in-href` |
| Location | `app/templates/courts/detail.html:82` (at detection) |
| Reported classification | Blocking; potential XSS through unsafe URL scheme |
| First detected | Phase 7 Exercise 4; exact date pending |
| Status | **Investigating — proposed false positive, not yet closed** |
| Owner / reviewer | To be recorded |
| Next review date | To be recorded |

**Observed behavior:** The template uses `href="{{ google_maps_url }}"`. Semgrep flags the variable because a URL supplied from an untrusted source could use a `javascript:` scheme. HTML escaping alone does not enforce safe URL schemes.

**Application-specific investigation:** The intended route calls `build_google_maps_url(court.location)` from `app/api/services/maps_service.py` and passes the resulting URL into the template. The Maps service is expected to use a fixed `https://www.google.com/maps/dir/` prefix with URL-encoded destination data. The court records' optional `google_maps_url` field should not be substituted as an unvalidated link.

**Evidence to record before disposition:**

- [ ] Confirm the current route passes only the URL returned by the trusted Maps service.
- [ ] Confirm the Maps service fixes the HTTPS scheme and Google Maps host and encodes destination input.
- [ ] Pass existing Maps service unit tests.
- [ ] Pass a malicious-looking address test confirming it cannot change the URL scheme or host.
- [ ] Pass the complete Pytest suite after the security test is added.
- [ ] Re-run Semgrep and record the actual finding count, version, date, and command.
- [ ] Record reviewer, rationale, and next review date for a final false-positive decision or remediation.

**Risk decision:** Do not change the status to `False Positive` merely because the current application is local or because tests pass. If the controls above are confirmed, document a rule-specific false-positive decision with evidence. If the URL can be controlled externally, remediate before closing. If Semgrep still reports the pattern, retain the finding and document its disposition; do not disable the full ruleset.

### 3.3 Phase 7 Exercise 4 — Step 11H Security Regression Verification

This section records final verification evidence for the frontend security review. Keep historical baselines in Section 2 unchanged. Update the pending entries **only after executing the relevant checks** on `feature/frontend-foundation`.

| Verification | Command or evidence | Recorded outcome | Status |
|---|---|---|---|
| Earlier regression baseline | `python -m pytest app/tests/ -q` | 42 passed, 1 `StarletteDeprecationWarning` (user-reported) | Passed at earlier checkpoint |
| Court-name HTML escaping | `python -m pytest app/tests/test_court_detail_web.py -k escapes -v` | Final targeted result not recorded | Pending |
| Court-address HTML escaping | Same targeted command; verify test collected | Final targeted result not recorded | Pending |
| Google Maps frontend security | `python -m pytest app/tests/test_court_detail_web.py -k google_maps -v` | Final targeted result not recorded | Pending |
| Maps service unit tests | `python -m pytest app/tests/unit/test_maps_service.py -v` | Final Step 11H result not recorded | Pending |
| Invalid query and court-ID tests | Targeted directory/detail Pytest checks | Final Step 11H result not recorded | Pending |
| Full regression suite after security changes | `python -m pytest app/tests/ -q` | New total not recorded; earlier baseline was 42 passed | Pending |
| Dependency consistency | `python -m pip check` | Previously reported passing; final Step 11H result not recorded | Pending |
| Semgrep rescan | `semgrep scan --config p/security-audit app/` | Final rescan result, date and version not recorded | Pending |

**Known test warning:** `StarletteDeprecationWarning` concerning `httpx`/`starlette.testclient` is tracked as dependency maintenance. It is not, by itself, a confirmed vulnerability or a failing test.

**SEC-FE-001 verification requirements:** Confirm that the frontend obtains the navigation URL exclusively from `build_google_maps_url(court.location)`; confirm the service fixes the HTTPS Google Maps origin and encodes destination data; execute the malicious-address regression test; and record the Semgrep rescan result. A passing Pytest suite does not automatically close the scanner finding.

**Evidence to complete:** Actual test counts, Semgrep version, scan date, Git commit SHA, finding count, local report path (if saved), reviewer, final disposition, and reassessment date. If the generic rule still flags the trusted dynamic `href`, document the rule-specific false-positive reasoning and decide how the blocking CI gate will handle the reviewed result. Do not disable the entire ruleset.

### 3.4 Finding Status Definitions

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

### 4.2 Phase 6 Terraform CI — Reported Passing; Evidence Metadata Pending

| Check | Intended enforcement | Verification status |
|---|---|---|
| Terraform formatting | Fail on formatting errors | Reported passed; run evidence pending |
| Terraform initialization | Fail on initialization errors | Reported passed; run evidence pending |
| Terraform validation | Fail on invalid configuration | Reported passed; run evidence pending |
| Trivy IaC scan | Report misconfigurations; scanner errors fail job | Reported passed; run evidence pending |

The user reported that all four CI jobs passed during Phase 6. Record the Terraform job run URL, commit SHA, tool versions, and any differences from the local IaC scan to complete the evidence trail. The Phase 7 Semgrep finding requires its own review and subsequent CI verification.

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
| ACT-010 | Record Terraform CI verification evidence | Medium | Evidence pending | Run URL, commit, formatting/validation/scan results |
| ACT-011 | Define IaC misconfiguration enforcement | Medium | Planned | Risk-based policy and thresholds |
| ACT-012 | Expand IaC controls for cloud deployment | Future | Planned | Cloud-specific security review and scan evidence |
| ACT-013 | Investigate and disposition `SEC-FE-001` | High | Investigating | URL data flow, negative test, Semgrep rescan, reviewer decision and date |
| ACT-014 | Record Phase 7 Semgrep scan metadata | Low | Open | Date, version, branch/commit, scan output |
| ACT-015 | Complete Step 11H final security regression evidence | Medium | Pending | Targeted and full test counts, dependency check, Semgrep rescan and SEC-FE-001 disposition |

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
| Not recorded | Semgrep `p/security-audit`, Phase 7 | `app/` | — | — | — | — | — | 1 blocking finding `SEC-FE-001`; severity counts not recorded; §2.5 |
<!-- Append a separate dated Phase 7 Semgrep rescan row after executing Step 11H; do not overwrite the initial finding. -->

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