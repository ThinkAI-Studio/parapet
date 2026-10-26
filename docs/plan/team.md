# Team

Three seats, sixteen weeks, one repository. **Two seats are filled as of
2026-10-26.**

## Team status

| Seat | GitHub | Active | Note |
| --- | --- | --- | --- |
| **TV1** | — | ❌ | Open. Full-stack seat; may stay empty for the whole sixteen weeks |
| **TV2** | `@anhkhoa` | ✅ | |
| **TV3** | `@bnhminh1010` | ✅ | |

Why this matters, stated plainly: the plan below was written for three people at
8–10 hours each (~400 hours). Two people is ~290 hours, a **~28% capacity cut**.
If TV1 is still empty at the M1 kickoff (week 3), the cut list in
[scope.md](scope.md#gate-rule) is applied from the start rather than at M9:

1. MCP server — dropped.
2. Telegram alerts — dropped (keep webhooks).
3. GitHub PR comment — dropped; Check Runs stay.
4. Attack Range — ships 4 scenarios, not 8.
(Mode B lab is already deferred outside the 16-week scope under ADR-0011.)

What is not cut: consent and verification, SSRF controls, the benchmark, the
security review, and the report itself. TV3 absorbs `apps/api`; TV2 absorbs the
minimum report UI needed to read a scan, and the landing page stays one static
page.

## Roles and ownership

| Member | Primary learning goal | Owns | Does not touch |
| --- | --- | --- | --- |
| **TV1** (open) | Refresh full-stack fundamentals | `apps/web`, landing page, report UI, Attack Range frontend | `infra/`, `services/scanner` |
| **TV2** | Systems, runtime, security engineering | `services/scanner` (Go), check implementations, rating engine, `services/lab` | `infra/` |
| **TV3** | Cloud, network, security, DevOps | `apps/api`, `infra/`, `bench/`, `attacks/`, CI/CD, observability, security review | check logic |

Shared: `packages/contracts`, `docs/`, `docs/adr/`.

Ownership is enforced by [`.github/CODEOWNERS`](../../.github/CODEOWNERS). Crossing
a boundary is allowed, but requires the owner's review — not a unilateral push.

## Interfaces between people

| Contract | Owner | Consumers |
| --- | --- | --- |
| `packages/contracts/openapi.yaml` | TV1 | TV2, TV3 |
| `packages/contracts/check-catalog.json` | TV2 | TV1, TV3 |
| `packages/contracts/schemas/*` | TV1 + TV2 | all |
| `infra/` outputs (endpoints, queue names) | TV3 | TV1, TV2 |

The rule: **TV1 is never blocked by infrastructure.** Local development runs on
Docker Compose from week 2. If the contract exists, TV1 can build against it.

## Ways of working

| Practice | Detail |
| --- | --- |
| Weekly sync | 30 minutes, Monday. Three lines each: done / blocked / next |
| Async updates | Written in the issue, not in chat |
| Pull requests | CI is the merge gate (`Docs`, `PR title`); a code owner reviews code |
| Branch naming | `feat/…`, `fix/…`, `docs/…`, `infra/…`, `chore/…` |
| Commits | Conventional Commits, one logical change; squash merge only |
| Issue-first | Non-trivial work starts as an issue linked to a milestone |
| Decision log | Any choice with a rejected alternative becomes an ADR |

## Definition of Ready

A story can start when:

- [ ] It has an ID in [user-stories.md](../product/user-stories.md)
- [ ] Acceptance criteria are written
- [ ] It is assigned to a milestone and a person
- [ ] External dependencies (contracts, infra) exist or have a stub

## Definition of Done

- [ ] Acceptance criteria met
- [ ] Tests added, or the exception explained
- [ ] `make check` passes
- [ ] Docs updated if behaviour changed
- [ ] Reviewed by a code owner
- [ ] No secrets or account identifiers committed

## Review pairing for SAA

Each week, TV2 and TV3 alternate:

1. **Designer** writes the AWS design for the week's milestone.
2. **Reviewer** attacks it with exam-style questions: *What happens if AZ-a
   fails? Why not Lambda? What does this cost at 10× traffic?*
3. The outcome is written as an ADR.

45 minutes, recorded in the ADR. This is the study method, not an extra meeting.

## Escalation

- Blocked more than one day → say so in the weekly sync thread, not at the next
  meeting.
- Disagreement on a technical decision → write the ADR with both options, the
  reviewer decides, and the decision is not revisited for the milestone.
- Disagreement on scope → [scope.md](scope.md) wins until it is changed by pull
  request.

## Health rules

- No one works alone on a security-critical component without review.
- Nobody deploys to production on a Friday evening.
- If two of three are unavailable, the third does documentation only.
- The project is a side project. Burnout is a bigger risk than a missed
  milestone.
