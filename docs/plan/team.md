# Team

Three people, sixteen weeks, one repository.

## Roles and ownership

| Member | Primary learning goal | Owns | Does not touch |
| --- | --- | --- | --- |
| **TV1** | Refresh full-stack fundamentals | `apps/web`, `apps/api`, landing page, report UI, Attack Range frontend | `infra/`, `services/scanner` |
| **TV2** | Systems, runtime, security engineering | `services/scanner` (Go), check implementations, rating engine, `services/lab` | `apps/web`, `infra/` |
| **TV3** | Cloud, network, security, DevOps | `infra/`, `bench/`, `attacks/`, CI/CD, observability, security review | `apps/web`, check logic |

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
| Pull requests | One reviewer; `docs/` may be self-merged; squash merge |
| Branch naming | `feat/…`, `fix/…`, `docs/…`, `infra/…`, `chore/…` |
| Commits | Conventional Commits, one logical change |
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
