# Contributing

Parapet is built by a team of three over sixteen weeks. The scope is locked
until week 16 (see [docs/plan/scope.md](docs/plan/scope.md)), so outside
contributions are limited to bug reports and documentation fixes until launch.
After launch, this document will grow a proper contributor guide.

## Before you start

Read, in this order:

1. [README.md](README.md) — what Parapet is and is not
2. [docs/product/brief.md](docs/product/brief.md) — who it is for
3. [docs/plan/scope.md](docs/plan/scope.md) — what is in and out of scope
4. [docs/product/non-goals.md](docs/product/non-goals.md) — what we refuse to build
5. [docs/plan/team.md](docs/plan/team.md) — who owns what

## Development setup

Local development runs entirely in Docker Compose. AWS is not required.

```bash
git clone https://github.com/ThinkAI-Studio/parapet.git
cd parapet
cp .env.example .env
make dev
```

`make dev` will be available from milestone M1. Until then, the repository
contains documentation only.

Requirements:

- Node.js 22+ and pnpm 9+
- Go 1.23+
- Docker 27+ with Compose v2
- Terraform 1.9+ (Mode B only)

## Ways of working

| Rule | Detail |
| --- | --- |
| Branches | `feat/…`, `fix/…`, `docs/…`, `chore/…`, `infra/…` |
| Commits | [Conventional Commits](https://www.conventionalcommits.org/) |
| Pull requests | One reviewer required; `docs/` may be self-merged |
| Merge strategy | Squash merge, one logical change per PR |
| Ownership | Enforced by [`.github/CODEOWNERS`](.github/CODEOWNERS) |
| Issue-first | Non-trivial work starts with an issue linked to a milestone |

Commit examples:

```
feat(scanner): add CORS reflection probe
fix(rating): correct HSTS severity when max-age is below 6 months
docs(adr): record DynamoDB decision
infra(terraform): add S3 gateway endpoint
```

## Definition of Done

A change is done when:

- [ ] It has tests, or the PR explains why it cannot
- [ ] `make check` passes locally (lint, typecheck, tests)
- [ ] Documentation is updated when behaviour changes
- [ ] New checks are added to the catalog with a standard mapping
- [ ] No secrets, tokens, account IDs or private hostnames are included
- [ ] A reviewer has approved

## Adding a security check

Every check must include, in `packages/contracts/check-catalog.json`:

- `id` — stable identifier, e.g. `TLS-03`
- `severity` — `critical` / `high` / `medium` / `low` / `info`
- `standard` — the published reference it enforces (NIST, OWASP, RFC)
- `evidence` — the raw artifact captured, so a finding can be reproduced
- `remediation` — concrete, copy-pasteable guidance

A check without a standard mapping will not be merged. See
`docs/security/standards-mapping.md` (written at M3).

## What we will not merge

- Code that exploits, brute forces, fuzzes, or degrades a third-party system
- Checks that scan ports other than 80, 443 and 53
- Features that require storing plaintext secrets
- Long-lived AWS access keys
- Anything listed in [docs/product/non-goals.md](docs/product/non-goals.md)

## Reporting security issues

Do not use issues or pull requests. See [SECURITY.md](SECURITY.md).

## Code of conduct

Participation is covered by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
