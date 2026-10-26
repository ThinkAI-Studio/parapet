# Architecture Decision Records

An ADR captures **one decision**, the context around it, and the alternatives we
rejected. If a decision has no rejected alternative, it probably does not need an
ADR.

## When to write one

Write an ADR when a choice is:

- expensive to reverse (data store, queue, hosting model),
- surprising to a new reader (why two modes? why no RDS?),
- a refusal (we will not build exploitation),
- the outcome of a design review.

Do not write an ADR for style choices. Those belong in
`docs/engineering/conventions.md` (written at M1).

## Format

```markdown
# NNNN. Short imperative title

- **Status:** Proposed | Accepted | Superseded by NNNN | Deprecated
- **Date:** YYYY-MM-DD
- **Deciders:** names

## Context

What forces are at play? Constraints, budget, learning goals, user needs.

## Decision

What we will do. One paragraph, present tense.

## Consequences

**Positive** — what gets better.
**Negative** — what we accept as a cost.
**Neutral** — what changes without being better or worse.

## Alternatives considered

1. **Option** — why rejected.
2. **Option** — why rejected.

## References

Links to standards, benchmarks or measurements that informed the decision.
```

## Index

| ADR | Title | Status |
| --- | --- | --- |
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-product-name-parapet.md) | Product name: Parapet | Accepted |
| [0003](0003-mode-a-serverless-as-production.md) | Mode A serverless as production, Mode B as lab | Accepted |
| [0004](0004-dynamodb-over-rds.md) | DynamoDB over RDS for Mode A | Accepted |
| [0005](0005-rating-model.md) | Rating model anchored to SSL Labs | Accepted |
| [0006](0006-scope-lock-16-weeks.md) | Scope lock: 16 weeks, AI in phase 2 | Accepted |
| [0007](0007-no-exploitation-policy.md) | No exploitation, ever | Accepted |
| [0008](0008-public-repository.md) | Public repository from day one | Accepted |
| [0009](0009-landing-page-hosting.md) | Landing page on Vercel first, S3 + CloudFront at M15 | Accepted |

## Conventions

- Numbers are sequential and never reused.
- Superseding a decision creates a new ADR that references the old one.
- An ADR is not edited after acceptance, except for typos and status changes.
