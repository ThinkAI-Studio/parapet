# Parapet

> **Prove your attack surface.**

Parapet scans what actually faces the internet — TLS, HTTP security headers,
DNS and email authentication — proves the impact with safe active probes and a
vulnerable-by-design range, verifies the fix, then keeps watching.

Built by [ThinkAI Studio](https://github.com/ThinkAI-Studio).

---

## Status

🚧 **Pre-alpha — week 0 of 16.** Nothing in this repository is ready for
production use. Follow progress in [docs/plan/roadmap.md](docs/plan/roadmap.md).

## Why Parapet exists

Most teams deploy a site and discover months later that HSTS was never enabled,
the certificate chain is broken, or any origin can read authenticated
responses.

Today's tools are one-shot. You scan once, get a letter grade, and forget it.
There is no history, no link to the deploy that caused the regression, and no
proof of what an attacker could actually do.

Parapet closes that loop:

```
Find  →  Prove  →  Fix  →  Verify  →  Track
```

- **Find** — 30 configuration checks across TLS, HTTP, DNS and email, each
  mapped to a published standard (NIST, OWASP, RFC).
- **Prove** — safe, read-only active probes, plus an isolated Attack Range that
  demonstrates impact against our own vulnerable-by-design targets. Never
  against yours.
- **Fix** — concrete remediation with config snippets, not a PDF.
- **Verify** — re-scan the exact check after you deploy.
- **Track** — grade history, per-commit correlation, drift alerts.

## What Parapet is not

- **Not a pentest tool.** No exploitation, ever. See
  [ADR-0007](docs/adr/0007-no-exploitation-policy.md).
- **Not a SAST or code-quality tool.** Parapet looks at what is running, not at
  your source. SonarQube checks code before deploy; Parapet checks what actually
  reached the internet.
- **Not highly available.** Single region, no SLA, three people, sixteen weeks.

Full list: [docs/product/non-goals.md](docs/product/non-goals.md).

## Architecture

Mode A runs on a verified zero-spend architecture inside always-free allowances. Mode B (the AWS lab) is deferred to a future roadmap outside the 16-week scope:

| Mode | Purpose | Stack |
| --- | --- | --- |
| **A — production** | serves real users, $0 baseline cost | Cloudflare (DNS, WAF, Pages), Lambda Function URL, DynamoDB (provisioned 25/25), Cloudflare R2, SQS, EventBridge, Telegram |
| **B — lab (deferred)** | AWS/SAA learning, future roadmap | VPC, ALB, ECS Fargate, RDS, ElastiCache, EC2 Spot, WAF (deferred) |

Details: [ADR-0011](docs/adr/0011-zero-spend-mode-a.md) and `docs/engineering/architecture.md` (written at M1).

## Repository layout

```
apps/          web dashboard, API handlers, landing page
services/      scan engine (Go), vulnerable-by-design lab, GitHub App
packages/      shared contracts: OpenAPI, schemas, check catalog
infra/         Mode A Terraform deployments (zero-spend)
bench/         benchmark corpus and SSL Labs comparison harness
attacks/       SSRF corpus and safe exploit demos used by the Range
docs/          product, plan, engineering, security, ops, ADRs
```

## Stack

| Layer | Choice |
| --- | --- |
| Web | Next.js, TypeScript on Cloudflare Pages (`app.parapet.thinkai.id.vn`) |
| API | AWS Lambda Function URL (Node/TypeScript) behind Cloudflare |
| Scan engine | Go |
| Data | DynamoDB (provisioned 25 RCU / 25 WCU), Cloudflare R2 (evidence) |
| Async | Amazon SQS, EventBridge |
| Edge & DNS | Cloudflare (DNS, WAF custom rules, 1 rate-limit rule, Pages) |
| Auth | Amazon Cognito User Pool (Essentials tier) |
| Alerts | Telegram webhook |
| Secrets | AWS Systems Manager Parameter Store (SecureString standard) |
| IaC | Terraform |
| CI/CD | GitHub Actions with OIDC — no long-lived keys |
| Observability | OpenTelemetry, CloudWatch |
## Documentation

Start at [docs/README.md](docs/README.md). The short version:

- [Product brief](docs/product/brief.md)
- [User stories](docs/product/user-stories.md)
- [Scope](docs/plan/scope.md) · [Roadmap](docs/plan/roadmap.md) · [Team](docs/plan/team.md)
- [Threat model](docs/security/threat-model.md)
- [Architecture decisions](docs/adr/README.md) · [Zero-spend (ADR-0011)](docs/adr/0011-zero-spend-mode-a.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Scope is locked until week 16; outside
contributions are welcome after launch.

## Security

Report vulnerabilities privately — see [SECURITY.md](SECURITY.md). Never open a
public issue for a security problem.

## License

[MIT](LICENSE) © ThinkAI Studio
