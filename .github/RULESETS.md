# Repository rulesets

The JSON files in `rulesets/` are **importable templates**. They do not change
any GitHub setting by themselves; the repository owner imports them once, on
purpose, after the CI workflows have run at least once so GitHub can resolve the
check names.

## Why there is no `develop` branch

Parapet is trunk-based with short-lived branches (`feat/`, `fix/`, `docs/`,
`infra/`, `chore/`), squash-merged into `master`. A long-lived `develop` branch
adds a second integration point that a two-person team does not need, and it
makes "which commit is in production" ambiguous during the sixteen weeks.

Releases are cut from `master` with an annotated `v*` tag, protected by
`rulesets/v-tags.json`.

## Import and activate

1. Open the repository, then **Settings** → **Rules** → **Rulesets**.
2. **New ruleset** → **Import a ruleset** → select `rulesets/master.json`, review
   the target and enforcement, then save.
3. Import `rulesets/v-tags.json` the same way. It makes release tags immutable
   after creation; a broken release is fixed by a new version, never by
   re-tagging history.
4. In the imported `master` ruleset, open **Require status checks to pass** and
   confirm the contexts match the job names in `.github/workflows/docs.yml`
   exactly:

   | Context | Workflow job |
   | --- | --- |
   | `Docs` | `docs` in `docs.yml` |
   | `PR title` | `pr-title` in `docs.yml` |

   Renaming a job without updating `rulesets/master.json` and the live ruleset
   leaves `master` permanently blocked. Treat the names as an API.
5. Keep **Require branches to be up to date** enabled. With two people and
   squash merges this costs one rebase per conflict, and it removes the class of
   bug where two individually green PRs break `master` together.

## The approval decision

`required_approving_review_count` is **0**, and CI is the merge gate. This is
deliberate, not an oversight:

- Two active maintainers, one open seat. Requiring an approval means one person
  can be blocked from shipping a docs fix while the other sleeps.
- The reference behaviour for this repository is "the checks must be green",
  which is enforceable and objective. A rubber-stamp approval is not a control.
- Review is still expected for code, and `.github/CODEOWNERS` records who should
  look. It is a social contract until there are three active maintainers.

**Trigger to change it:** when the TV1 seat is filled and three people are
active, raise `required_approving_review_count` to `1` and set
`require_code_owner_review` to `true`. That is a ruleset change in a pull
request, not a quiet settings edit.

## Adding checks as the code lands

`Docs` and `PR title` are the only checks that exist in a docs-only repository.
Add the real gates to `required_status_checks` **after** the workflow producing
them has run on `master` at least once:

| Milestone | Workflow | Job names to add |
| --- | --- | --- |
| M1 | `ci.yml` | `Web quality`, `Go quality`, `Go race` |
| M1 | `codeql.yml` | `CodeQL` |
| M2 | `ssrf.yml` | `SSRF corpus` (must be 40/40 blocked) |
| M9 | `bench.yml` | `Benchmark agreement` |

Do not add a check name before the workflow exists — GitHub will wait for a
status that never arrives, and the branch is stuck.

## Required repository settings

Set once by the owner, not versioned here:

- **Settings → Code security:** secret scanning, push protection, Dependabot
  alerts and security updates, private vulnerability reporting. All enabled on
  2026-10-26.
- **Settings → General:** squash merge only, delete branch on merge, allow
  auto-merge.
- **Settings → Actions:** read-only `GITHUB_TOKEN` by default; workflows opt into
  more with an explicit `permissions:` block.

## What the ruleset cannot express

- **Docs may be self-merged** (see `CONTRIBUTING.md`). Rulesets have no
  path filters, so this is a convention, not a control. The protection that
  matters — no direct push to `master`, no force push, no deletion — applies to
  everything.
- **Release provenance.** `master` gating does not prove a tag points at a
  reachable commit. When `release.yml` is added at M13 it must re-check ancestry,
  the same way the release workflow in `HomeLab-Minh` does.
- **Scope.** A ruleset cannot reject a feature that crosses
  `docs/product/non-goals.md`. That is what review and ADR-0006 are for.
