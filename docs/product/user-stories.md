# User Stories

Single source of truth for product behaviour. There is no separate PRD: each
story carries its own spec notes, edge cases and telemetry.

**Change rule:** a story may only be added or changed in a pull request that
also updates [scope.md](../plan/scope.md) if the milestone moves.

## Personas

| ID | Persona | Primary need |
| --- | --- | --- |
| **P1** | Indie developer — 1–5 domains, deploys on Vercel/Netlify/VPS | Know what to fix first, and understand why |
| **P2** | Small-team developer — ships daily, has CI, no security specialist | Block regressions at deploy time |
| **P3** | Security learner — student or junior | See attacks work safely |
| **P4** | Abuser — wants to scan a domain they do not own | Must be blocked and recorded |

## Epic map

| Epic | Stories | Milestone |
| --- | --- | --- |
| E1 — Onboarding and ownership proof | US-01 | M2 |
| E2 — Assessment and report | US-02, US-04 | M3–M5 |
| E3 — Proof of impact | US-03, US-08 | M6–M10 |
| E4 — Verification loop | US-05 | M8 |
| E5 — CI/CD integration | US-06, US-07 | M7 |
| E6 — Monitoring and alerts | US-09 | M8 |
| E7 — Distribution | US-10 | M15 |
| E8 — Operations | US-11 | M11 |
| E9 — Abuse prevention | US-12 | M2 |

## Story index

| ID | Title | Persona | Priority |
| --- | --- | --- | --- |
| US-01 | Add and verify a domain | P1 | P0 |
| US-02 | Get a grade and a prioritised list | P1 | P0 |
| US-03 | Prove impact without touching your site | P1 | P0 |
| US-04 | Get remediation I can paste | P1 | P0 |
| US-05 | Confirm a fix actually worked | P1 | P0 |
| US-06 | Gate deploys in CI | P2 | P0 |
| US-07 | See which commit changed the grade | P2 | P1 |
| US-08 | Practise attacks in a safe range | P3 | P1 |
| US-09 | Get alerted when a grade drops | P1 | P1 |
| US-10 | Publish a report and a badge | P1 | P1 |
| US-11 | Understand cost per scan | Operator | P1 |
| US-12 | Scan a domain I do not own | P4 | P0 |

---

## E1 — Onboarding and ownership proof

### US-01 — Add and verify a domain

**Persona:** P1 · **Epic:** E1 · **Milestone:** M2 · **Priority:** P0

**Story**
As an indie developer, I want to add my domain and prove I control it, so that
Parapet can scan it without becoming a tool for scanning strangers.

**Acceptance criteria**

- Given I am signed in, when I submit `example.com`, then I get a verification
  token and instructions for a DNS TXT record at `_parapet.example.com`.
- Given the TXT record is present, when I click verify, then the domain becomes
  `verified` and its first scan is queued within 60 seconds.
- Given the TXT record is missing, then verification fails with the exact value
  we looked for and the resolver we queried.
- Given a domain is unverified, then no scan of any kind is ever dispatched.

**Spec notes**

- Verification is a DNS TXT lookup, not an HTTP file, because it must work
  before the site is reachable.
- Tokens are 32 random bytes, base32 encoded, stored hashed.
- Re-verification is required every 90 days, and on ownership dispute.

**Edge cases**

- CNAME to a DNS provider that strips TXT → show both TXT and HTTP fallback.
- Multiple TXT records at the same name → any match verifies.
- Domain already verified by another account → require TXT proof again, do not
  reveal the other account.

**Out of scope**

- Scanning without verification, including "just one quick check".
- Wildcard verification covering subdomains.

**Telemetry**

`domain_added`, `domain_verified{attempts}`, `domain_verification_failed{reason}`.
Success: ≥ 80% of added domains verified within 24 hours.

---

## E2 — Assessment and report

### US-02 — Get a grade and a prioritised list

**Persona:** P1 · **Epic:** E2 · **Milestone:** M5 · **Priority:** P0

**Story**
As an indie developer, I want one grade plus a short prioritised list, so that I
know what to fix first instead of reading thirty rows.

**Acceptance criteria**

- Given a completed scan, then I see a grade from A to F and a score from 0 to
  100.
- Given more than five findings, then the report shows at most five "fix first"
  items, ordered by severity and exploitability.
- Given a finding, then I can expand it to see the raw evidence captured.
- Given a check that produced no finding, then I can still see it under
  "passed" so I know it was tested.

**Spec notes**

- Grade is a weighted sum over four categories, published in
  [ADR-0005](../adr/0005-rating-model.md).
- Severity comes from OWASP Risk Rating (likelihood × impact), not CVSS.
- Every finding links to the standard it violates.

**Edge cases**

- Scan partially failed (for example DNS timeout) → grade is `incomplete`, never
  a misleading letter.
- Site behind a CDN → evaluate the edge response, and say so in the report.

**Out of scope**

- Trend charts (that is US-09).
- Custom severity overrides.

**Telemetry**

`report_viewed{domain_id}`, `finding_expanded{check_id}`.
Success: median time from first report to first fix under 10 minutes.

---

### US-04 — Get remediation I can paste

**Persona:** P1 · **Epic:** E2 · **Milestone:** M5 · **Priority:** P0

**Story**
As an indie developer, I want copy-pasteable configuration for my stack, so that
I can fix the issue without becoming a TLS expert.

**Acceptance criteria**

- Given a finding, then I see at least one snippet relevant to a detected stack
  (nginx, Caddy, Next.js, Cloudflare).
- Given the stack cannot be detected, then I see the generic snippet plus a note
  that detection failed.
- Given a snippet, then copying it produces valid syntax for that tool.
- Given a fix is applied, then a "Verify fix" action re-runs only the affected
  checks.

**Spec notes**

- Snippets are stored as templates with the finding ID as key, versioned in the
  repository, reviewed like code.
- Stack detection is best-effort from headers and server banners; it never
  changes the grade.

**Edge cases**

- Multiple stacks (Next.js behind nginx) → show both, labelled by layer.
- Snippet conflicts with another finding → surface the conflict.

**Out of scope**

- Applying the fix for the user.
- Generating snippets for arbitrary frameworks.

**Telemetry**

`snippet_copied{check_id, stack}`, `verify_clicked{check_id}`.
Success: copy rate above 25% on failing checks.

---

## E3 — Proof of impact

### US-03 — Prove impact without touching your site

**Persona:** P1 · **Epic:** E3 · **Milestone:** M9 · **Priority:** P0

**Story**
As an indie developer, I want to see what an attacker could actually do, so that
I understand severity without reading TLS documentation.

**Acceptance criteria**

- Given a finding with a demo available, when I click "Show me the impact", then
  a sandboxed demo opens against `lab-*.parapet.dev`.
- Given the demo runs, then it shows the raw request and response, and the
  concrete consequence (cookie read, framed page, redirect to a look-alike).
- Given the demo runs, then **no request is sent to my domain**.
- Given the demo finishes, then I can open "How to fix" from the same panel.
- Given the lab is unreachable, then I see an explanation, never a silent
  failure.

**Spec notes**

- Range targets come from a fixed allowlist resolved server-side, never from
  user input.
- Demo assets are static; no scan data is rendered inside the iframe.
- Only findings marked `demo_available` in the catalog get the button.

**Edge cases**

- Finding already fixed → demo remains available, labelled "sample".
- User's browser blocks third-party frames → show a full-page fallback.

**Out of scope**

- Running the exploit against the user's own domain.
- User-supplied payloads.

**Telemetry**

`demo_opened{check_id}`, `demo_completed{check_id, duration_ms}`.
Success: > 40% of users who open a demo then click "Verify fix".

---

### US-08 — Practise attacks in a safe range

**Persona:** P3 · **Epic:** E3 · **Milestone:** M10 · **Priority:** P1

**Story**
As a security learner, I want a place where I can run real attacks against
deliberately broken targets, so that I understand the mechanics without breaking
the law or someone's site.

**Acceptance criteria**

- Given the Range index, then I see 8 scenarios with difficulty and the concept
  each one teaches.
- Given a scenario, then I can run the attack, see the request, and see the
  captured result.
- Given I finish a scenario, then it links to the matching Parapet check so I
  can test my own site for the same issue.
- Given the Range, then a banner states clearly that every target is owned by
  ThinkAI Studio and intentionally vulnerable.

**Spec notes**

- Scenarios: missing CSP, clickjacking, CORS reflection, open redirect, cookie
  without `Secure`/`HttpOnly`, weak TLS, dangling CNAME, directory listing.
- Rate limited per session; no scenario accepts arbitrary targets.

**Edge cases**

- Scenario service down → degrade to a static walkthrough with screenshots.

**Out of scope**

- CTF scoring, leaderboards, user accounts on the Range.
- Scenarios that require exploitation beyond a proof of concept.

**Telemetry**

`range_scenario_started{id}`, `range_scenario_completed{id}`.
Success: ≥ 30% of Range visitors convert to a verified domain.

---

## E4 — Verification loop

### US-05 — Confirm a fix actually worked

**Persona:** P1 · **Epic:** E4 · **Milestone:** M8 · **Priority:** P0

**Story**
As an indie developer, I want to re-scan after deploying, so that I know the fix
worked instead of hoping.

**Acceptance criteria**

- Given a finding, when I click "Verify fix", then only the affected checks are
  re-run.
- Given the check now passes, then the finding moves to `verified` and the grade
  updates.
- Given the check still fails, then I see the new evidence next to the old one.
- Given a verification is requested twice within a minute, then the second
  request is deduplicated.

**Spec notes**

- Verification scans are separate records, linked to the parent scan.
- A finding stays `open` until a verification passes; nothing auto-closes.

**Edge cases**

- CDN cache still serving the old configuration → report the response we saw,
  with the `Age` and `Cache-Control` headers as evidence.

**Out of scope**

- Automatic re-verification on a timer (that is drift detection, US-09).

**Telemetry**

`verify_started{check_id}`, `verify_result{check_id, passed}`, time to verify.
Success: median time from fix to verified under 3 minutes.

---

## E5 — CI/CD integration

### US-06 — Gate deploys in CI

**Persona:** P2 · **Epic:** E5 · **Milestone:** M7 · **Priority:** P0

**Story**
As a small-team developer, I want Parapet to check my deployment, so that a
security regression blocks the pull request instead of reaching users.

**Acceptance criteria**

- Given the GitHub App is installed on a repository linked to a verified domain,
  when a deployment succeeds, then a scan runs against the deployed URL.
- Given the grade is below the configured threshold, then the check run
  concludes `failure` with a link to the report.
- Given the grade is acceptable, then the check run concludes `success`.
- Given the scan cannot run, then the check run concludes `neutral`, never
  `failure` (a broken scanner must not block deploys).

**Spec notes**

- GitHub App permissions: `checks:write`, `contents:read`, `pull_requests:read`,
  `deployments:read`, `metadata:read`.
- Installation tokens are short-lived and never logged.
- Threshold defaults to the grade of the previous scan on the default branch.

**Edge cases**

- Preview URLs must match a pattern registered in `.parapet.json`, otherwise the
  scan is refused.
- Two deployments in quick succession → only the latest commit is gated.

**Out of scope**

- GitLab, Bitbucket, Azure DevOps.
- Blocking merges at the branch-protection level on the user's behalf.

**Telemetry**

`ci_scan_triggered{repo}`, `ci_check_conclusion{result}`, `ci_scan_refused{reason}`.
Success: installed on ≥ 3 real repositories.

---

### US-07 — See which commit changed the grade

**Persona:** P2 · **Epic:** E5 · **Milestone:** M7 · **Priority:** P1

**Story**
As a small-team developer, I want each scan tied to a commit, so that I can find
the change that caused a regression.

**Acceptance criteria**

- Given a scan triggered by a deployment, then it stores `repo`, `commit_sha`,
  `ref` and `environment`.
- Given a grade change between two scans, then the report shows the commit range
  between them.
- Given a commit, then I can see the findings it introduced and resolved.

**Spec notes**

- Correlation is by deployment event, not by polling; polling creates false
  attribution.
- Unattributed scheduled scans are labelled `scheduled`, not guessed.

**Out of scope**

- Reading source diffs to explain the cause.
- Auto-bisect.

**Telemetry**

`commit_attributed{repo}`, `regression_attributed{repo}`.
Success: ≥ 90% of grade changes attributable to a commit.

---

## E6 — Monitoring and alerts

### US-09 — Get alerted when a grade drops

**Persona:** P1 · **Epic:** E6 · **Milestone:** M8 · **Priority:** P1

**Story**
As an indie developer, I want to be told when my grade drops, so that I react
before my users notice.

**Acceptance criteria**

- Given a verified domain, then I can choose a cadence (daily by default).
- Given a scheduled scan produces a lower grade than the previous one, then an
  alert is sent within 5 minutes.
- Given the same finding fails twice in a row, then I receive one alert, not
  two.
- Given the alert, then it names the domain, the previous and current grade, and
  the top three changed findings.

**Spec notes**

- Drift is defined as a grade change or a new critical/high finding.
- Alerts go to email (SES) and an optional webhook (Discord/Slack).
- Unsubscribing from alerts does not stop scheduled scans.

**Edge cases**

- Scanner error → no alert, but an internal alarm fires instead. Never alert the
  user about our failure as if it were their problem.
- Domain expired → alert once with a specific reason.

**Out of scope**

- SMS and phone calls.
- On-call escalation policies.

**Telemetry**

`alert_sent{channel, reason}`, `alert_deduped`, `alert_clicked`.
Success: false-positive alerts under 2% of sends.

---

## E7 — Distribution

### US-10 — Publish a report and a badge

**Persona:** P1 · **Epic:** E7 · **Milestone:** M15 · **Priority:** P1

**Story**
As an indie developer, I want a public report and a badge, so that I can show
the result and share it with my team or my users.

**Acceptance criteria**

- Given a verified domain, then I can publish a read-only report at an
  unguessable URL.
- Given the report is published, then a badge SVG is available for embedding.
- Given I unpublish, then both the report and the badge return 404 within 60
  seconds.
- Given the badge is fetched, then it caches for 60 seconds at the edge.

**Spec notes**

- Public reports are served from S3 through CloudFront with Origin Access
  Control; the bucket is never public.
- Publishing is opt-in per domain and never includes raw evidence by default.

**Edge cases**

- Domain re-verified by another account → old public link is revoked.
- Badge requested for a private domain → generic "not public" badge.

**Out of scope**

- Custom branding, custom domains, PDF export.

**Telemetry**

`report_published`, `badge_served{domain_id}`, `report_unpublished`.
Success: ≥ 20% of verified domains publish a report.

---

## E8 — Operations

### US-11 — Understand cost per scan

**Persona:** Operator (team) · **Epic:** E8 · **Milestone:** M11 · **Priority:** P1

**Story**
As the operator, I want to see cost per scan and per domain, so that I can keep
the free tier honest and know when the architecture must change.

**Acceptance criteria**

- Given a month of scans, then I can see total cost, cost per 1,000 scans, and
  cost per verified domain.
- Given a cost anomaly, then a budget alarm fires before the monthly budget is
  exhausted.
- Given the Mode A versus Mode B comparison, then the crossover point is
  documented with measured numbers.

**Spec notes**

- Cost data comes from Cost Explorer and CUR; the scan count comes from
  DynamoDB, not from an estimate.
- Every resource is tagged `project=parapet`, `env`, `owner`.

**Edge cases**

- Free-tier credits distort the number → report both gross and net cost.

**Out of scope**

- Per-user billing.

**Telemetry**

`cost_report_generated`; published monthly in `docs/ops/cost.md`.

---

## E9 — Abuse prevention

### US-12 — Attempt to scan a domain I do not own

**Persona:** P4 (negative) · **Epic:** E9 · **Milestone:** M2 · **Priority:** P0

**Story**
As an abuser, I want to scan a domain I do not control, so that Parapet must stop
me and record the attempt.

**Acceptance criteria**

- Given an unverified domain, when any scan is requested, then the request is
  rejected with `403 domain_not_verified`.
- Given repeated attempts, then the account is rate limited and flagged after
  five failures in an hour.
- Given the same target is attempted from many accounts, then the target is
  temporarily blocked and the operator is notified.
- Given an attempt, then it is logged with account, target, timestamp and source
  IP, retained for 90 days.

**Spec notes**

- Rejection happens before any DNS resolution or TCP connection to the target.
- Rate limits are enforced per account and per target independently.
- The target allowlist is the only path to the scan engine; the queue consumer
  re-checks verification.

**Edge cases**

- Legitimate ownership transfer → manual review path, not an exception in code.

**Out of scope**

- Legal escalation workflow.

**Telemetry**

`scan_rejected{reason}`, `abuse_flagged{account_id}`.
Success: 100% of unverified scan attempts rejected, verified in CI.
