# Scope

Locked at M0. Changes require a pull request that names the milestone it moves
and the work it displaces.

## In scope

| Area | Detail |
| --- | --- |
| **Assessment** | 30 checks: TLS (12), HTTP headers (8), DNS (5), email (5). Each mapped to NIST, OWASP or an RFC |
| **Proof** | 9 safe read-only active probes (weak handshake, CORS reflection, open redirect, HTTP methods, dangling CNAME, AXFR, ALPN, SRI, mixed content; SMTP STARTTLS explicitly deferred to Mode B) |
| **Proof (lab)** | Attack Range with 8 vulnerable-by-design scenarios, browser demos, no third-party targets |
| **Verification** | Re-run the affected checks after a fix, close the finding |
| **Tracking** | Grade history, diff, drift alerts, finding lifecycle with SLA |
| **CI/CD** | GitHub App: repo ↔ domain, commit correlation, Check Runs, PR comment |
| **Distribution** | Public report, badge SVG, REST API, MCP server (stretch) |
| **Evidence** | Benchmark against SSL Labs on a 120-domain corpus, published confusion matrix |
| **Infrastructure** | Mode A serverless zero-spend in production (ADR-0011); Mode B AWS lab deferred to future roadmap |
| **Docs** | Product, plan, engineering, security, ops, ADRs, runbooks |

## Out of scope

See [non-goals](../product/non-goals.md) for the reasoning. Summary:

- Exploitation of any kind
- Source code analysis (SAST), code quality
- AI features (phase 2)
- Multi-region active-active, SLA
- Organisations, SSO, RBAC, billing
- Mobile applications
- Scanning ports other than 80, 443, 53
- Storing customer page content
- A general-purpose chat assistant
- Mode B lab (deferred to future roadmap, outside 16-week scope and budget)

## Definition of Done (project)

Measured at week 16 from real usage.

| # | Metric | Target |
| --- | --- | --- |
| 1 | Verified domains | ≥ 50 |
| 2 | Weekly active users | ≥ 30 |
| 3 | Total scans | ≥ 10,000 |
| 4 | Grade agreement with SSL Labs (120 domains) | ≥ 95% |
| 5 | SSRF payloads blocked in CI | 40 / 40 |
| 6 | Attack Range scenarios working | 8 / 8 |
| 7 | p95 scan latency | < 10 s |
| 8 | Production cost | $0 inside always-free allowances |
| 9 | GitHub App installed on real repositories | ≥ 3 |
| 10 | Game days with written postmortem | ≥ 2 |
| 11 | ADRs recorded | ≥ 12 |

If a metric is missed, it is reported as missed with the reason. It is not
quietly redefined.

## Budget

Mode B is out of scope. Production operates on a verified $0 baseline inside always-free allowances.

| Component | Free allowance | Ceiling |
| --- | --- | --- |
| Edge, TLS, DNS, WAF (Cloudflare) | Unlimited requests, custom WAF rules, 1 rate-limit rule | $0.00 / month |
| Landing & hosting (Cloudflare Pages) | Unlimited static requests, 100 custom domains | $0.00 / month |
| API compute (AWS Lambda Function URL) | 1,000,000 requests and 400,000 GB-seconds per month (about 3.2M seconds only at 128 MB; always-free) | $0.00 / month |
| Evidence & report storage (Cloudflare R2) | 10 GB storage, 1M Class A, 10M Class B ops, $0 egress | $0.00 / month |
| Database (AWS DynamoDB) | 25 RCU, 25 WCU provisioned capacity, 25 GB storage (always-free) | $0.00 / month |
| Queue (AWS SQS) | 1,000,000 requests/month standard queue (always-free) | $0.00 / month |
| Secrets (AWS SSM Parameter Store) | Standard parameters, standard throughput (always-free) | $0.00 / month |
| Auth (AWS Cognito User Pool) | Essentials tier, 10,000 MAU, built-in email ~50/day (always-free) | $0.00 / month |
| Alerts (Telegram webhook) | Bot API, unlimited messages within rate limits | $0.00 / month |
| CI/CD (GitHub Actions + OIDC) | Public repository free runner minutes | $0.00 / month |
| **Total baseline** | **All components inside always-free allowances** | **$0.00 / month** |

AWS Budgets zero-spend alert set at $0.01 to catch any accidental paid service creation immediately.
## Gate rule

At the end of each milestone, if the milestone is not met, **cut scope — do not
extend the deadline.**

Cut order:
1. MCP server
2. Telegram alerts (keep webhooks)
3. GitHub PR comment (keep Check Runs)
4. Attack Range scenarios 5–8 (ship 4)
Never cut: consent and verification, SSRF controls, benchmark, or the security
review in M12.

## Assumptions

1. 16 weeks at ~8–10 hours per person per week. Written for three people
   (~400 hours); as of 2026-10-26 only two seats are filled (~290 hours), so the
   contingency in [team.md](team.md#team-status) applies.
2. Production cost $0 inside always-free allowances for the project (ADR-0011).
3. Team is comfortable with Linux CLI at a basic level; if not, add one week of
   Linux and networking basics before M1.
4. Repository is public from day one.
