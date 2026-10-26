# Backlog

**This file is a view, not the source of truth.**

The source of truth is [GitHub Issues](https://github.com/ThinkAI-Studio/parapet/issues)
and the current milestone. This file is refreshed every Monday and is allowed to
be stale by a week. Do not edit it to track work.

## Current milestone

_Updated 2026-10-26 — week 1._

| ID | Item | Owner | Status |
| --- | --- | --- | --- |
| M0-1 | [Docs scaffold and repository hygiene](https://github.com/ThinkAI-Studio/parapet/issues/7) | TV3 | ✅ Done |
| M0-2 | [Check catalog with standard mapping](https://github.com/ThinkAI-Studio/parapet/issues/2) | TV2 | ⬜ Todo |
| M0-3 | [Threat model v0 review](https://github.com/ThinkAI-Studio/parapet/issues/3) | TV3 | ⬜ Todo |
| M0-4 | [AWS account, budget, tagging](https://github.com/ThinkAI-Studio/parapet/issues/4) | TV3 | ⬜ Todo |
| M0-5 | [OpenAPI contract and report mock](https://github.com/ThinkAI-Studio/parapet/issues/5) | TV1 → TV3 | ⬜ Todo |
| M0-6 | [Landing page v0](https://github.com/ThinkAI-Studio/parapet/issues/6) | TV1 → TV3 | ⬜ Todo |

## Next up

| Item | Milestone | Notes |
| --- | --- | --- |
| Docker Compose dev stack | M1 | Terraform + DynamoDB Local, ElasticMQ, MinIO, API, worker |
| DynamoDB single-table design | M1 | Needs ADR-0004 follow-up with access patterns |
| First 10 TLS checks | M1 | Cert chain, protocols, ciphers, HSTS |
| GitHub Actions OIDC role | M1 | No long-lived keys |
| DNS TXT verification flow | M2 | Blocking for everything else |

## Open decisions (need an ADR)

These are known, scoped and unowned. Each blocks a milestone, and each becomes
an ADR rather than a chat decision.

| Decision | Blocks | Issue |
| --- | --- | --- |
| SSL Labs benchmark logistics and quota | M9 | [#11](https://github.com/ThinkAI-Studio/parapet/issues/11) |
| Legal terms, abuse contact, takedown path | M2 | [#12](https://github.com/ThinkAI-Studio/parapet/issues/12) |

## Not doing now

Items that are deliberately parked. They are not forgotten; they are refused
for the current scope. See [non-goals](../product/non-goals.md).

- AI triage and patch PRs (phase 2)
- Second region
- Organisations and SSO
- Public API keys for third parties
- Mode B AWS lab (deferred to future roadmap)
