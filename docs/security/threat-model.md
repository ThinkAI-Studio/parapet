# Threat Model (v0)

Status: **Draft** — reviewed at the end of every milestone.
Owner: TV3, with TV2 for anything touching the scan engine.
Method: STRIDE, plus an abuse-case review for the scanning capability itself.

## 1. What we are protecting

| Asset | Why it matters | Impact if lost |
| --- | --- | --- |
| **User accounts** | Email, session, linked repositories | Account takeover, unauthorised scans |
| **Verified domains** | The list of targets users authorised | Abuse, reputational and legal damage |
| **Scan evidence** | Certificates, headers, DNS records | Third-party data exposure |
| **GitHub installation tokens** | Write access to users' checks | Ability to post false results in their CI |
| **AWS credentials and roles** | Full control of our infrastructure | Cost blowout, data loss, use as an attack platform |
| **The scan engine's network position** | It can reach arbitrary hosts by design | Becoming an SSRF proxy or a DDoS tool |
| **Attack Range** | Intentionally vulnerable services | Being used to pivot into our own network |

## 2. Actors

| Actor | Capability | Motivation |
| --- | --- | --- |
| Curious user | Normal account | Understand their own site |
| Abuser (P4) | Normal account, many accounts, or no account | Scan a target they do not own, use us as a proxy |
| Opportunistic attacker | Internet access | Free compute, credentials, data |
| Malicious scanned site | Controls the content we fetch | Attack the scanner through its input |
| Insider | Repository and cloud access | Accidental misconfiguration, leaked secret |

## 3. Trust boundaries

```
Internet
  │
  ├──[1] CloudFront / API Gateway ──> Lambda API ──> DynamoDB
  │                                        │
  │                                        └──> SQS
  │
  ├──[2] GitHub webhooks ──────────> Lambda (HMAC verified)
  │
  └──[3] Target site ──────────────> Scan engine ──> S3 evidence
                                          │
                                          └──[4] Attack Range (own network)
```

| # | Boundary | Rule |
| --- | --- | --- |
| 1 | Public to API | Authenticated, rate limited, schema validated |
| 2 | GitHub to API | Signature verified, replay protected, installation scoped |
| 3 | Scan engine to target | **Untrusted both ways**: target input is hostile, our egress is privileged |
| 4 | Scan engine to Range | Isolated network; a compromise here must not reach data stores |

## 4. STRIDE analysis

| Threat | Example | Mitigation |
| --- | --- | --- |
| **Spoofing** | Forged GitHub webhook triggers scans | HMAC-SHA256 `X-Hub-Signature-256`, secret in Secrets Manager, delivery ID deduplication |
| **Tampering** | Modified scan result in transit or at rest | TLS everywhere, S3 SSE-KMS, versioning, write-only worker role |
| **Repudiation** | Abuser claims they never requested a scan | Append-only audit log with account, target, IP, timestamp, 90-day retention |
| **Information disclosure** | Public report leaks raw evidence or another user's domain | Public reports opt-in, unguessable IDs, OAC-only bucket, no raw evidence by default |
| **Denial of service** | Flooding the API or the queue | WAF rate rules, per-account quotas, SQS DLQ, worker concurrency caps |
| **Elevation of privilege** | Worker role used to read the database | Worker has no DB credentials; only SQS receive, S3 put on one prefix, logs |
| **SSRF** | User submits `http://169.254.169.254/` | Resolve, deny-list private ranges, pin IP, re-check on every redirect |
| **Prompt injection** (phase 2) | Scanned page contains "ignore previous instructions" | Never feed raw HTML; parsed fields only; structured output; no write tools |

## 5. Abuse of the scanning capability

This is the highest-risk area, because the product's purpose is to make
outbound requests.

| Control | Detail |
| --- | --- |
| Consent | DNS TXT at `_parapet.<domain>` required before any request |
| Ports | Only 80, 443, 53, and SMTP STARTTLS to the MX |
| Methods | Read-only: `GET`, `HEAD`, `OPTIONS`, `TRACE` to `/` only |
| Redirects | Maximum 5, re-resolved and re-checked at each hop |
| Rate | 1 request/second per target, 1 scan/hour per domain |
| Payloads | No injection strings, no fuzzing, no credential attempts |
| Detection | Repeated unverified attempts flag the account and the target |
| Kill switch | A single feature flag pauses all scanning |

## 6. SSRF control detail

1. Resolve the hostname and collect **all** A and AAAA records.
2. Reject if any address is in `10/8`, `172.16/12`, `192.168/16`, `100.64/10`,
   `169.254/16`, `127/8`, `0.0.0.0/8`, `::1`, `fc00::/7`, `fe80::/10`, or is a
   known cloud metadata address.
3. Pin the resolved IP and connect to it directly, setting SNI and the `Host`
   header manually.
4. On every redirect, resolve again and repeat steps 1–3.
5. Cap time at 15 s, headers at 64 KB, body at 1 MB.
6. Reject non-HTTP schemes.

The corpus in `attacks/ssrf/` is run in CI on every pull request. Target: 40/40
blocked.

## 7. Residual risks (accepted, for now)

| Risk | Why accepted | Revisit |
| --- | --- | --- |
| No WAF in Mode A initially | Cost; CloudFront rate limiting covers the common case | M10 |
| Single region | Cost; documented as a deliberate limitation | Never in this scope |
| Scan engine has broad egress by design | It is the product. Compensated by no credentials, netns isolation and flow logs | Reviewed every milestone |
| No formal pen test of our own API | Time; compensated by ASVS checklist and internal review | M12 |
| Email deliverability | SES sandbox; DKIM/SPF/DMARC configured | M6 |

## 8. Review log

| Date | Milestone | Change |
| --- | --- | --- |
| 2026-10-26 | M0 | Initial model |
