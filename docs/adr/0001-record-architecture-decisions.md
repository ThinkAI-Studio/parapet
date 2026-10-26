# 0001. Record architecture decisions

- **Status:** Accepted
- **Date:** 2026-10-26
- **Deciders:** TV1, TV2, TV3

## Context

Three people, sixteen weeks, two distinct learning goals. Decisions will be made
quickly and asynchronously, often in conversation. Without a written record, the
same debate will happen three times and the reasoning will be lost by the time
we write it on a CV.

The project also has a public repository, so decisions are visible to anyone
reading the code.

## Decision

Every decision that is expensive to reverse, surprising, or a refusal is
recorded as an ADR in this directory, using the template in
[README.md](README.md). One decision per file.

## Consequences

**Positive**

- New readers understand *why*, not just *what*.
- Disagreements end at the ADR instead of resurfacing weekly.
- The rejected alternatives are exactly the material an SAA exam asks about.
- Writing for an external reader forces clearer thinking.

**Negative**

- Around 30–45 minutes per decision, unpaid.
- Risk of writing ADRs for trivial things; the "no rejected alternative" rule
  prevents most of it.

**Neutral**

- ADRs live next to the code and are reviewed in the same pull request.

## Alternatives considered

1. **A wiki or Notion page** — drifts from the code, no review, no history in
   the repository.
2. **Commit messages only** — too short for context and alternatives.
3. **No record** — the default, and the reason most side projects cannot explain
   their own architecture six months later.

## References

- Michael Nygard, *Documenting Architecture Decisions* (2011)
