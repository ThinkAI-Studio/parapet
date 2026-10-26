# Non-Goals

Things we deliberately will not build. Each one is a decision, not an
oversight. Revisit only when the stated condition becomes true.

| # | Non-goal | Why | Revisit when |
| --- | --- | --- | --- |
| NG-01 | **Exploitation** of any kind — SQLi, XSS, brute force, fuzzing, DoS, request smuggling | Illegal without explicit authorisation, harmful to third parties, and destroys the trust model that lets us scan at all. See [ADR-0007](../adr/0007-no-exploitation-policy.md) | Never |
| NG-02 | **Source code analysis** (SAST), code quality, code smells | Different domain. SonarQube, Semgrep and CodeQL are years ahead. Our advantage is external and black-box | Never — integrate instead |
| NG-03 | **AI features** in the 16-week scope | Does not teach AWS, networking, systems or security; adds cost and a new attack surface (prompt injection). Deferred to phase 2 | After the SAA exam |
| NG-04 | **Multi-region active-active** or HA with an SLA | Cost and complexity with no learning return at this scale. Mode B documents the production design instead | If the service ever has paying users |
| NG-05 | **Organisations, SSO, RBAC, billing** | Only one user type is needed to validate the product | After 50 weekly active users |
| NG-06 | **Mobile applications** | The web report is already responsive; nothing to learn | Never |
| NG-07 | **Scanning non-web services** beyond SMTP STARTTLS | Port scanning beyond 80/443/53 looks like an attack and triggers abuse reports | Never |
| NG-08 | **Storing customer content** beyond scan artifacts | Privacy liability with no product value. We store findings and evidence, not pages | Never |
| NG-09 | **A general-purpose chat assistant** | Demo-friendly, unmeasurable, and does not differentiate. AI, if added, is narrow and evaluated | Phase 2, only with a metric |
| NG-10 | **Supporting every language and framework** in remediation snippets | Four good snippets beat twenty bad ones | When users ask, by demand |

## How to use this file

When someone proposes a feature, the first question is: *does it cross a
non-goal?* If yes, link the row and close the discussion. If the proposal is
genuinely valuable, the correct move is to change the non-goal in a pull
request — with an ADR — not to quietly make an exception.
