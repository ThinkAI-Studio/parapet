# 0006. Scope lock: 16 weeks, AI in phase 2

- **Status:** Accepted
- **Date:** 2026-10-26
- **Deciders:** TV1, TV2, TV3

## Context

Three people, a side project, roughly 8–10 hours per person per week. Two of
them are also preparing for AWS SAA-C03 during the same period, at about 5 hours
per week. That leaves an effective capacity of roughly 400–450 person-hours for
the entire product.

Side projects fail in a predictable way: the scope grows to match the
enthusiasm of week 2, then stalls in week 9 with nothing deployable. The
temptation is always the same set of additions — AI, more checks, more
integrations, a nicer dashboard — and each one is individually reasonable.

There is also a hard external date: the SAA exam sits in weeks 17–18. Project
work cannot extend into study time without putting both goals at risk.

## Decision

The project scope is **frozen at M0 for sixteen weeks** and contains **P0 and a
small, named set of P1 items only**. The freeze is explicit and written down in
[scope.md](../plan/scope.md).

Rules:

1. **P0 only ships.** P1 items — commit correlation, the Range learner track,
   drift alerts, badges, cost reporting — ship only if the milestone that owns
   them is met without borrowing time from a later milestone.
2. **AI is deferred to phase 2**, after the SAA exam. No LLM calls, no embeddings,
   no prompt code in the sixteen-week scope. If AI is added later it must be one
   narrow, measurable feature (finding triage or a remediation PR), evaluated
   against a baseline.
3. **Deadlines do not move; scope does.** At the end of a milestone: met →
   proceed; partially met → cut from the published cut list; not met on the
   critical path → stop and re-plan in the same week.
4. **The cut list is ordered in advance**, so the decision is not made under
   pressure: MCP server → second region → email alerts → PR comment → Range
   scenarios 5–8 → Mode B burst 2.
5. **Never cut**: consent and verification, SSRF controls, the benchmark, the
   M12 security review. These are the product's licence to operate.
6. **Adding scope requires a pull request** that names the item it displaces and
   updates [scope.md](../plan/scope.md) in the same change. No verbal exceptions.

## Consequences

**Positive**

- There is a single answer to "should we also…": read the cut list.
- The security-critical core is protected by rule 5, so cutting never makes the
  product unsafe.
- Phase 2 has a clean starting point: a working product, real users, real scan
  data, and a benchmark to evaluate AI against.
- The discipline itself is a deliverable — a written scope lock with a cut order
  is what separates a shipped project from a repository of half-features.
- Study time is protected, which protects the exam.

**Negative**

- We will say no to good ideas, repeatedly, and some of them will be genuinely
  better than what we build.
- P1 items that users might value (badges, alerts) may not ship at all.
- Deferring AI costs some portfolio appeal in the short term; the counter-
  argument is a shipped product with numbers, which is stronger.
- A 16-week fixed window with three people leaves no slack for illness. The
  buffer week is the only slack, and it is not enough for two lost weeks.

**Neutral**

- Phase 2 is not scheduled; it starts after the exam and gets its own scope
  document.

## Alternatives considered

1. **24 weeks, everything included** — more relaxing, but collides with the exam
   and with the natural attention span of a side project. Rejected: a longer
   deadline mostly produces a later stall.
2. **Ship a smaller product in 8 weeks, then iterate** — attractive, but eight
   weeks does not reach the benchmark, the Range, or the AWS lab, which are the
   three things that make the project verifiable and worth writing about.
   Rejected.
3. **Include AI now, as the differentiator** — the most common advice, and wrong
   for this team: it teaches nothing about AWS, networking or systems, it adds
   cost and a new attack surface (prompt injection via scanned content), and it
   is hard to evaluate without real scan data. Rejected; revisit in phase 2.
4. **No fixed deadline, ship when ready** — no forcing function, no cut order,
   and the exam date stops being a constraint on the project. Rejected.
5. **Full SAST/DAST suite as well** — duplicates mature tools and crosses a
   non-goal. Rejected.

## References

- [Scope](../plan/scope.md)
- [Roadmap](../plan/roadmap.md)
- [Non-goals](../product/non-goals.md)
- [SAA learning plan](../team/learning-plan.md)
