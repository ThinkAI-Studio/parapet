# 0008. Public repository from day one

- **Status:** Accepted
- **Date:** 2026-10-26
- **Deciders:** TV1, TV2, TV3

## Context

The repository has two jobs: hold the code, and serve as the team's portfolio.
Two of the members are studying for AWS SAA-C03 and will be job-hunting
afterwards; a public repository with real users, a published benchmark and a
readable history is stronger evidence than a private one described in an
interview.

The counter-arguments are real:

- **Security.** We are building a security product. Publishing the design
  invites scrutiny, and a mistake in a public repo is visible to everyone.
- **Secrets.** A public repo means one careless `git add` publishes a credential
  to the world, permanently.
- **Abuse.** Publishing an SSRF corpus and Range payloads gives someone a
  starter kit.
- **Expectation.** Public means people can open issues, expect support, and
  judge the work before it is finished.
- **Competition.** Anyone can read the roadmap and copy it.

There is also a timing question: publish from day one, or publish a polished
snapshot at launch.

## Decision

The repository is **public from the first commit** at
`github.com/ThinkAI-Studio/parapet`, under **MIT**. Documentation is written for
an external reader from the start, in English, and progress is visible including
the parts that are unfinished.

The launch is a *product* event (week 15), not a *repository* event. The repo is
public; the product is pre-alpha and says so on every page.

### What we accept as a consequence

| Risk | Mitigation |
| --- | --- |
| Secret committed | GitHub secret scanning + push protection enabled before the second commit; no secrets in the repo by design — everything comes from environment variables or Secrets Manager; AWS access via GitHub OIDC, so there are no long-lived keys to leak |
| Attacker reads our design | The threat model is public on purpose. Security by obscurity is not a control we are relying on; the controls are verification, allowlists, rate limits and isolation |
| Someone reuses the SSRF corpus to attack | The corpus is defensive test data — a list of payloads to *block*. It is already widely published. The Range payloads run only against our own lab and are useless without our allowlist |
| Public criticism of unfinished work | The README states pre-alpha, week 0 of 16, with a link to the roadmap. Unfinished is the expected state, not a surprise |
| Copied roadmap | Execution, users and the benchmark are the moat, not the idea. A copied roadmap is a compliment |
| Support expectations | `CONTRIBUTING.md` says external contributions are limited to bugs and docs until launch |
| Employer or client discomfort | Nothing here is confidential; no employer code, data, account IDs or hostnames are used. The AWS account is personal, funded by credits |
| History rewritten later to hide mistakes | We do not rewrite public history. Mistakes get a follow-up commit and, when interesting, a note in the changelog |

### Rules that make "public" safe

1. **No secrets, ever.** `.env.example` only; `.gitignore` covers `.env*`, keys,
   state files and tfvars. Secret scanning blocks the push.
2. **No real user data in the repo.** Benchmarks store domain names (public by
   nature) and score summaries; raw evidence stays in S3 with a retention rule.
3. **No employer or client material.** Personal AWS account, own domain, own lab.
4. **No account IDs, ARNs with IDs, or internal hostnames** in committed docs or
   Terraform. Use variables and placeholders.
5. **Security issues go through private reporting**, not public issues — see
   `SECURITY.md`.
6. **Commit messages are written as if a hiring manager will read them**, because
   they might.

## Consequences

**Positive**

- The portfolio value starts on day one, not at launch.
- Documentation written for strangers is better documentation: clearer, less
  reliant on context only the authors have.
- Public review is free review; a reader who spots a flaw in the threat model has
  done us a favour.
- Hiring managers can see the decisions, not just the result — the ADRs are the
  most transferable artefact in the repository.
- The pressure of visibility is a real forcing function against scope creep and
  abandoned branches.
- MIT means anyone can self-host, which is a distribution channel we could not
  buy.

**Negative**

- Every mistake is public and permanent, including the ones made while learning.
- Competitors can read the plan and ship first.
- We must maintain a minimum standard of hygiene from commit one: no debug
  secrets, no "WIP" branches left dangling, no broken links in the README.
- Some readers will treat pre-alpha software as production and file issues about
  it. Triage cost is real.
- Recruiters may read early commits. That is the point, and also the risk.

**Neutral**

- The license was already MIT on the remote; this ADR confirms it rather than
  changing it.
- Public does not mean "accepting contributions"; the contribution policy is
  separate and stricter.

## Alternatives considered

1. **Private until launch, then open source** — the safer default, and what most
   teams do. Rejected: it removes the forcing function, hides the most
   interesting part (the decisions and the mistakes), and gives nine months of
   work zero portfolio value until week 15.
2. **Public code, private design docs** — splits the source of truth and makes
   the ADRs unreadable in context. Rejected.
3. **Source-available, not open source (e.g. BSL)** — protects against a
   competitor hosting it, but discourages exactly the individual users we want,
   and adds licence complexity for no measurable benefit at this scale.
   Rejected; MIT is a distribution decision, not a revenue decision.
4. **Public now, but with a sanitised git history rewritten before launch** —
   rewriting public history destroys the credibility the repository exists to
   build, and is easy to detect. Rejected.
5. **Public with no documentation until the product works** — cheapest to start,
   and the reason so many projects are unreadable six months in. Rejected: the
   documentation is the deliverable.

## References

- [README](../../README.md), [SECURITY.md](../../SECURITY.md),
  [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [Threat model](../security/threat-model.md)
- [Scope: assumptions](../plan/scope.md#assumptions)
- GitHub Docs: *About secret scanning* and *Push protection*
