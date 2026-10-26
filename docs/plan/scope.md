# Scope

Locked at M0. Changes require a pull request that names the milestone it moves
and the work it displaces.

## In scope

| Area | Detail |
| --- | --- |
| **Assessment** | 30 checks: TLS (12), HTTP headers (8), DNS (5), email (5). Each mapped to NIST, OWASP or an RFC |
| **Proof** | 10 safe read-only active probes (weak handshake, CORS reflection, open redirect, HTTP methods, dangling CNAME, AXFR, SMTP STARTTLS, ALPN, SRI, mixed content) |
| **Proof (lab)** | Attack Range with 8 vulnerable-by-design scenarios, browser demos, no third-party targets |
| **Verification** | Re-run the affected checks after a fix, close the finding |
| **Tracking** | Grade history, diff, drift alerts, finding lifecycle with SLA |
| **CI/CD** | GitHub App: repo ↔ domain, commit correlation, Check Runs, PR comment |
| **Distribution** | Public report, badge SVG, REST API, MCP server (stretch) |
| **Evidence** | Benchmark against SSL Labs on a 120-domain corpus, published confusion matrix |
| **Infrastructure** | Mode A serverless in production; Mode B AWS lab in two bursts |
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
| 8 | Production cost | < $15 / month |
| 9 | GitHub App installed on real repositories | ≥ 3 |
| 10 | Game days with written postmortem | ≥ 2 |
| 11 | ADRs recorded | ≥ 10 |

If a metric is missed, it is reported as missed with the reason. It is not
quietly redefined.

## Budget

| Item | Cost |
| --- | --- |
| Mode A production ($5/month × 4 months) | $20 |
| Mode B lab, burst 1 (10 days × $4.50) | $45 |
| Mode B lab, burst 2 (10 days × $4.50) | $45 |
| Domain | $12 |
| SSL Labs API, SES, GitHub, Vercel | $0 |
| **Total** | **~$122** |

Funded by AWS credits. AWS Budgets alerts at 50%, 80% and 100%, plus a budget
action that stops lab EC2 instances.

## Gate rule

At the end of each milestone, if the milestone is not met, **cut scope — do not
extend the deadline.**

Cut order:

1. MCP server
2. Second region (Mode B)
3. Email alerts (keep webhooks)
4. GitHub PR comment (keep Check Runs)
5. Attack Range scenarios 5–8 (ship 4)
6. Mode B burst 2

Never cut: consent and verification, SSRF controls, benchmark, or the security
review in M14.

## Assumptions

1. 16 weeks at ~8–10 hours per person per week. Written for three people
   (~400 hours); as of 2026-10-26 only two seats are filled (~290 hours), so the
   contingency in [team.md](team.md#team-status) applies.
2. AWS spend under ~$150 total for the project.
3. Team is comfortable with Linux CLI at a basic level; if not, add one week of
   Linux and networking basics before M1.
4. Repository is public from day one.
