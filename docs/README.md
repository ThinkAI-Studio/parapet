# Documentation

Single entry point for everything that is not code.

**Rule:** every document has an owner and a review cadence. A document without
an owner gets deleted, not left to rot.

## Read in this order

| If you want to know… | Read |
| --- | --- |
| What Parapet is, in two minutes | [../README.md](../README.md) |
| Why it exists and who it is for | [product/brief.md](product/brief.md) |
| Exactly what we are building | [product/user-stories.md](product/user-stories.md) |
| What we refuse to build | [product/non-goals.md](product/non-goals.md) |
| What is in scope and when it is done | [plan/scope.md](plan/scope.md) |
| Who does what, which week | [plan/roadmap.md](plan/roadmap.md), [plan/team.md](plan/team.md) |
| What can go wrong, security-wise | [security/threat-model.md](security/threat-model.md) |
| Why a decision was made | [adr/README.md](adr/README.md) |
| How the two of us study for SAA | [team/learning-plan.md](team/learning-plan.md) |

## Index

| File | Question it answers | Owner | Cadence | Status |
| --- | --- | --- | --- | --- |
| `product/brief.md` | Why does this exist, for whom? | All | On positioning change | Active |
| `product/user-stories.md` | What exactly must the product do? | All | Per milestone | Active |
| `product/non-goals.md` | What will we not build, and why? | All | When tempted | Active |
| `plan/scope.md` | In, out, and definition of done | All | Every milestone | Active |
| `plan/roadmap.md` | Who does what, which week | TV3 | Every Monday | Active |
| `plan/team.md` | Ownership and ways of working | All | On process change | Active |
| `plan/backlog.md` | What is next (view of GitHub Issues) | TV3 | Every Monday | Active |
| `security/threat-model.md` | How could we be attacked? | TV3 + TV2 | Every milestone | Draft |
| `team/learning-plan.md` | What do we study this week | TV2 + TV3 | Weekly | Active |
| `adr/*.md` | Why we chose X over Y | Decision owner | When decided | Active |

## Planned documents

Created in the milestone where they become true. Do not create empty files.

| File | Created at | Purpose |
| --- | --- | --- |
| `engineering/architecture.md` | M1 | Mode A and Mode B diagrams, component responsibilities |
| `engineering/data-model.md` | M1 | DynamoDB single-table design and access patterns |
| `engineering/conventions.md` | M1 | Code style, error format, naming |
| `engineering/testing.md` | M3 | Test pyramid, fixtures, golden files |
| `security/standards-mapping.md` | M3 | Every check mapped to NIST / OWASP / RFC |
| `security/consent-and-abuse.md` | M2 | Domain verification, rate limits, abuse handling |
| `security/secure-sdlc.md` | M4 | Our own SAST/SCA/secret scanning gates |
| `legal/terms.md` | M2 | Authorisation clause for scanning |
| `legal/privacy.md` | M2 | What user data we store and for how long |
| `ops/environments.md` | M10 | Accounts, regions, environments |
| `ops/observability.md` | M12 | Metrics, traces, dashboards |
| `ops/slo.md` | M12 | SLIs, SLOs, error budget |
| `ops/cost.md` | M11 | Cost per scan, budget model |
| `ops/game-days.md` | M12 | Failure exercises and results |
| `ops/runbooks/` | M12 | One runbook per alert |

## Conventions

- **Language:** English, everywhere in the repository. Notes in chat may be in
  Vietnamese; anything committed is English.
- **Decisions:** one file per decision in [`adr/`](adr/README.md).
- **Dates:** ISO 8601 (`2026-10-26`).
- **Units:** milliseconds for latency, USD for cost, UTC for timestamps.
- **Links:** relative links inside the repository, so they work on forks. Every
  relative link and `#anchor` is checked in CI — run
  `python3 .github/scripts/check_links.py` before pushing.
- **CI:** the required checks and branch rules are documented in
  [`.github/RULESETS.md`](../.github/RULESETS.md). A planned document is
  referenced as `code`, not as a link, until it exists.
