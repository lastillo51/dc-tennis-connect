# DC Tennis Connect — Repository Snapshot Management Runbook

**Status:** Phase 8 Exercise 6, prepared for review (2026-11-25).  
**Source snapshot:** `21e53c4534bd989ff1df5c7422960b85cd9f30b8`.

## Purpose

Maintain a verifiable, point-in-time archive of the committed DC Tennis Connect repository for project reviews, documentation updates, troubleshooting, and handoffs. A ZIP snapshot is **not** a live GitHub connection and does not automatically incorporate later commits.

## Before exporting

From `~/projects/dc-tennis-connect`:

```bash
git branch --show-current
git fetch origin
git status --untracked-files=all
git rev-parse HEAD
git rev-parse origin/feature/postgresql-court-data
```

Check that intended files are committed and the working tree is clean. If commit hashes differ, investigate before describing the archive as synchronized. `git archive HEAD` includes committed content at `HEAD`; it omits untracked and uncommitted changes.

## Create and inspect a snapshot

```bash
git archive --format=zip --output=/tmp/dc-tennis-connect-project.zip HEAD
unzip -l /tmp/dc-tennis-connect-project.zip | less
```

For a documentation-only archive:

```bash
git archive --format=zip --output=/tmp/dc-tennis-phase8-documentation.zip HEAD \
  README.md docs/requirements/project-requirements.md \
  docs/requirements/feature-backlog.md docs/architecture/system-overview.md \
  docs/architecture/frontend-overview.md docs/architecture/database-overview.md \
  docs/security/security-policy.md docs/runbooks/security-findings.md
```

Before distributing an archive, inspect filenames and contents for `.env` files, credentials, keys, tokens, database dumps, Terraform state, local reports, personal information, and downloaded GIS artifacts. **A Git archive is not automatically secret-safe:** sensitive information already committed to Git can appear in the archive. Stop and remediate any exposure before sharing. Never include local database backups or secret configuration files.

## Record and distribute the snapshot

Store or share the reviewed ZIP through an approved project file-sharing location. Record the following metadata alongside it:

- Repository name: `dc-tennis-connect`.
- Branch name (for example, `feature/postgresql-court-data` or `main`).
- Exact commit SHA from `git rev-parse HEAD`.
- Snapshot creation date and archive filename.
- Test and CI results associated with that SHA, verified independently.
- Whether uncommitted local changes were intentionally excluded.

For code or documentation reviews, identify the snapshot and target files. Review proposed changes or replacement files locally, run relevant tests, and commit only after verification. Do not assume an archived snapshot reflects later GitHub activity.

## Refresh after a major exercise, pull request, or merge

Generate a new ZIP from the updated, verified commit. Record which earlier snapshot it supersedes. After merging into `main`, use the verified `main` commit SHA as the canonical baseline. Retain older snapshots only when needed for traceability and label them to avoid version confusion.

## Validation checklist

- [ ] Correct repository and branch identified.
- [ ] Commit SHA recorded and remote synchronization checked where applicable.
- [ ] No unexpected modified or untracked implementation files.
- [ ] Archive filenames and contents inspected for sensitive information.
- [ ] Tests and CI status recorded separately from the snapshot.
- [ ] Snapshot location and exact commit recorded in project handoff notes.
- [ ] Documentation distinguishes implemented features from planned work.

## Recover from mismatched snapshots

If a review references missing importer modules, outdated migrations, or inconsistent documentation, compare the archive file listing and recorded commit SHA with the current repository. Regenerate the snapshot from the intended commit and redistribute it. Do not change application code merely to match an obsolete archive.