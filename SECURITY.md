# Security Policy

## Supported versions

Parapet is pre-alpha and has no supported release yet. Once a version is
published, this table will list the versions that receive security fixes.

| Version | Supported |
| --- | --- |
| `main` (pre-alpha) | ⚠️ development only — no security guarantees |

## Reporting a vulnerability

**Do not open a public issue, discussion, or pull request for a security
problem.**

Use GitHub's private vulnerability reporting:

1. Go to the **Security** tab of this repository.
2. Click **Report a vulnerability**.
3. Include: affected component, reproduction steps, impact, and any suggested
   fix.

If private reporting is unavailable to you, email the maintainers listed in
[`CODEOWNERS`](.github/CODEOWNERS) and ask for a private channel. Do not include
exploit details in that first email.

### What to expect

| Stage | Target |
| --- | --- |
| Acknowledgement | 3 business days |
| Initial assessment | 10 business days |
| Fix or documented mitigation | 30 days for high/critical |
| Public disclosure | coordinated with you, after a fix ships |

This is a side project with three maintainers. We will be honest if we cannot
meet a timeline rather than go silent.

## Scope

**In scope — Parapet itself:**

- The web application, API and public report pages
- The scan engine and its network isolation controls
- The GitHub App and webhook handling
- Infrastructure and IAM configuration in this repository
- The Attack Range services (they are intentionally vulnerable, but must not be
  usable to attack anything outside the Range)

**Out of scope:**

- Vulnerabilities in domains scanned by Parapet. We do not own those systems;
  contact their operator. If a finding is a false negative or false positive,
  open a regular issue.
- Denial of service through ordinary load. Report capacity problems as bugs.
- Findings that require a compromised maintainer account, physical access, or a
  already-rooted host.
- Missing security headers on the `lab.*` hosts. They are vulnerable on purpose.

## Safe harbour for researchers

We will not pursue or support legal action against researchers who:

- test only accounts and domains they own or have explicit permission to test,
- avoid privacy violations, data destruction, and service degradation,
- give us reasonable time to fix the issue before disclosure,
- do not exploit a finding beyond what is needed to demonstrate it.

If in doubt, ask first. We would rather answer a question than receive a
surprise.

## Our own practices

Parapet is a security product, so the repository holds itself to the same bar:

- Threat model reviewed every milestone — [docs/security/threat-model.md](docs/security/threat-model.md)
- No long-lived AWS credentials; CI uses GitHub OIDC
- Secret scanning and push protection enabled
- Dependency and container scanning in CI
- Least-privilege IAM, reviewed at M9 — see [docs/plan/roadmap.md](docs/plan/roadmap.md)

## What Parapet will never do

Parapet performs configuration assessment and safe, read-only probes. It does
not exploit, brute force, fuzz, or attempt denial of service against any target.
This is a product decision documented in
[ADR-0007](docs/adr/0007-no-exploitation-policy.md), not a temporary limitation.
