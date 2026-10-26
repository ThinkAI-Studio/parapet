# Product Brief

One page. If this changes, the project has changed.

## Problem

A developer deploys a website and has no idea how it looks from the outside.
Weeks later they discover that HSTS was never enabled, the certificate chain is
incomplete, or any origin can read authenticated responses.

The tools that exist today are one-shot:

- **SSL Labs** grades TLS, then forgets you.
- **Mozilla Observatory** and **securityheaders.com** check headers once.
- **Uptime monitors** tell you the site is up, not whether it is safe.

None of them answer three questions a developer actually has:

1. Did I get worse since last week, and which deploy did it?
2. What could an attacker *actually do* with this misconfiguration?
3. Did my fix work?

## Users

| Persona | Description | Primary need |
| --- | --- | --- |
| **P1 — Indie developer** | 1–5 domains, deploys on Vercel/Netlify/VPS, self-taught | Know what to fix first, and understand why |
| **P2 — Small team developer** | Ships daily, has CI, no security specialist | Block security regressions at deploy time |
| **P3 — Security learner** | Student or junior, wants practical understanding | See attacks work in a safe environment |
| **P4 — Abuser (negative)** | Wants to scan a domain they do not own | Must be blocked, and the attempt recorded |

P1 is the design target. P2 justifies the GitHub integration. P3 justifies the
Attack Range. P4 shapes the threat model.

## Solution

```
Find  →  Prove  →  Fix  →  Verify  →  Track
```

| Step | What happens |
| --- | --- |
| **Find** | 30 checks across TLS, HTTP, DNS, email, each mapped to a published standard |
| **Prove** | Safe read-only probes against the user's domain; impact demonstrated against our own lab |
| **Fix** | Remediation with copy-pasteable config for nginx, Caddy, Next.js, Cloudflare |
| **Verify** | Re-run the exact check after deploy, and close the finding |
| **Track** | Grade history, per-commit correlation, drift alerts |

## Differentiation

| | SSL Labs | Observatory | Security Headers | **Parapet** |
| --- | --- | --- | --- | --- |
| TLS assessment | ✅ deep | ➖ | ➖ | ✅ |
| Header assessment | ➖ | ✅ | ✅ | ✅ |
| Continuous monitoring | ❌ | ❌ | ❌ | ✅ |
| Commit correlation | ❌ | ❌ | ❌ | ✅ |
| Proof of impact | ❌ | ❌ | ❌ | ✅ safe demos |
| Remediation with config | ➖ | ➖ | ➖ | ✅ |
| Verification loop | ❌ | ❌ | ❌ | ✅ |
| Open source | ❌ | ✅ | ❌ | ✅ MIT |

The defensible part is the loop, not any single check. Anyone can copy a list of
headers; copying the loop, the range and the benchmark is work.

## Success criteria

Measured at week 16, from real usage — not estimates.

| Metric | Target |
| --- | --- |
| Verified domains | ≥ 50 |
| Weekly active users | ≥ 30 |
| Total scans | ≥ 10,000 |
| Grade agreement with SSL Labs (120-domain corpus) | ≥ 95% |
| Attack Range scenarios working | 8 / 8 |
| SSRF payloads blocked in CI | 40 / 40 |
| p95 scan latency | < 10 s |
| Production cost | < $15 / month |

## Risks

| Risk | Mitigation |
| --- | --- |
| Rating diverges from the industry standard | Anchor the model to SSL Labs categories; publish a confusion matrix and every discrepancy |
| Perceived as an illegal scanning tool | DNS TXT verification, strict rate limits, safe-only probes, published terms |
| Scope creep toward pentesting or SAST | Hard non-goals plus an ADR for each refusal |
| No real users, so no real numbers | Waitlist from the landing page; personal network; two language communities |
| Team runs out of time between the project and the SAA exam | Scope lock at 16 weeks, gate rule that cuts features rather than extending deadlines |

## What success looks like in one sentence

A developer adds a domain, learns in two minutes what is wrong and what it
would cost them, fixes it, and proves the fix — and the same thing happens
automatically on their next deploy.
