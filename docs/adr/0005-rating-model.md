# 0005. Rating model anchored to SSL Labs

- **Status:** Accepted
- **Date:** 2026-10-26
- **Deciders:** TV1, TV2, TV3

## Context

A grade is the product's most visible claim. If Parapet says **B** and SSL Labs
says **A**, users lose trust immediately and we cannot defend the number. If the
grade is a simple count of failed checks, it is easy to explain but sells the
wrong thing: a missing `X-Frame-Options` would outweigh a broken certificate
chain.

Three properties matter, in this order:

1. **Defensible** — every point must trace to a published standard and a captured
   piece of evidence.
2. **Comparable** — the result must be checkable against an external, independent
   implementation.
3. **Explainable** — a user must be able to see why they got the score they got.

There is no public specification for "overall web security grade". SSL Labs is
the de facto reference for TLS, but it does not assess headers, DNS or email. So
we cannot copy a formula; we can only anchor to one and extend it transparently.

## Decision

Parapet computes **one score (0–100), one letter grade (A–F), and four category
sub-scores**. The TLS sub-score is deliberately anchored to SSL Labs so that the
two can be compared directly.

### Category weights

| Category | Weight | Rationale |
| --- | --- | --- |
| **TLS** | 40 | Highest impact when wrong: it breaks confidentiality outright |
| **HTTP** | 25 | Directly enables client-side attacks (framing, injection, leakage) |
| **Email** | 20 | Spoofing and phishing damage happens even when the site is perfect |
| **DNS** | 15 | Enables takeover and trust failures; lower frequency, high severity |

Weights sum to 100. Category score = 100 − Σ(check weight × severity multiplier)
for failed checks in that category, floored at 0. Passed and not-applicable
checks contribute nothing.

### Severity multipliers

| Severity | Multiplier | Typical example |
| --- | --- | --- |
| `critical` | 3.0 | Certificate chain invalid, private key exposed |
| `high` | 2.0 | TLS 1.0 enabled, no HSTS, SPF missing |
| `medium` | 1.0 | Weak cipher suite, missing CSP |
| `low` | 0.5 | Missing `X-Content-Type-Options` |
| `info` | 0.0 | Observable but not scored |

Multipliers exist so that a single critical failure can dominate a category
without the model needing per-check bespoke maths. Each check declares its own
base weight (1–10) in the check catalogue at
`packages/contracts/check-catalog.json`, together with its severity and its
standard reference. The catalogue is reviewed like code.

### Letter grade

| Score | Grade |
| --- | --- |
| 90–100 | **A** |
| 80–89 | **B** |
| 70–79 | **C** |
| 60–69 | **D** |
| 50–59 | **E** |
| 0–49 | **F** |

### Caps and overrides

Numeric scores can hide a fatal flaw, so four rules override the number:

| Rule | Effect |
| --- | --- |
| Any `critical` finding in TLS | Grade capped at **C**, score capped at 79 |
| Certificate invalid, expired, or hostname mismatch | Grade **F**, regardless of score |
| Any `critical` finding in any category | Grade capped at **B** |
| Scan incomplete (a category could not be assessed) | Grade **`incomplete`**, never a letter |

`incomplete` is a first-class result, not an error. It is stored, shown, and
excluded from benchmark comparisons. A grade is never invented from partial
data.

### Comparison with SSL Labs

The benchmark compares **Parapet's TLS category letter** against **SSL Labs'
overall letter**, on a fixed 120-domain corpus.

Normalisation for comparison:

- SSL Labs `A+` and `A-` collapse to `A`.
- SSL Labs `T` (untrusted) and `M` (hostname mismatch) collapse to `F`.
- SSL Labs `R` (revoked) is excluded from the corpus, as it is a moving target.

Agreement means the same letter after normalisation. Target: **≥ 95%** across the
corpus, with the full confusion matrix published in
`bench/results/` and in the README.

Every disagreement gets a written reason in the benchmark report, classified as:

| Class | Meaning | Action |
| --- | --- | --- |
| `our-bug` | We parsed or graded incorrectly | Fix the check; add a regression fixture |
| `model-gap` | We do not test what SSL Labs tests (e.g. some cipher scoring) | Document; consider adding the check |
| `their-bug` | SSL Labs is wrong or stale | Document with evidence; no change |
| `n/a` | Site changed between the two measurements | Re-run; exclude if it persists |

Rules that keep the benchmark honest:

- The corpus is fixed and published **before** the model is tuned. Adding a
  domain later requires a note explaining why.
- The model is never adjusted per domain. A change that improves agreement on
  one domain must be justified by a category rule, then re-run on all 120.
- Both measurements happen within the same hour, from the same region.
- The rating model is versioned (`rating_version` is stored on every scan), so a
  historical grade can still be explained after the model changes.

## Consequences

**Positive**

- The grade is comparable to a tool users already trust, and we publish where we
  disagree.
- Every point is traceable to a check, a severity and a standard.
- Category sub-scores let the report say *"your TLS is fine, your email is not"*
  instead of a single opaque number.
- Versioning means history survives model changes.
- Publishing the confusion matrix turns the weakest part of the product into a
  credibility asset.

**Negative**

- The weights are a judgement call. They are defensible but not provable, and we
  must say so openly.
- Chasing 95% agreement may push us toward SSL Labs' peculiarities rather than
  correctness. Mitigated by requiring a category-level reason for any change.
- Two grading systems (score and caps) create edge cases that need tests, e.g. a
  score of 95 with an invalid certificate is still `F`.
- The 120-domain corpus needs maintenance as domains expire or change owners.

**Neutral**

- `incomplete` propagates into alerts: an incomplete scan never triggers a
  drift alert (see US-09).
- The score is recomputed on read from stored findings when `rating_version`
  differs, so old scans can be re-graded without a migration.

## Alternatives considered

1. **Count of failed checks** — trivially explainable, but weights a missing
   `X-Content-Type-Options` the same as an expired certificate. Rejected: it
   would make the product confidently wrong.
2. **CVSS scores everywhere** — precise for individual vulnerabilities, but CVSS
   is designed for exploitable software flaws, not configuration posture, and it
   gives no aggregate grade. Rejected as the wrong tool; OWASP Risk Rating
   (likelihood × impact) is used per finding instead.
3. **Cope SSL Labs' formula exactly** — impossible: the formula is unpublished
   and covers only TLS. An approximation presented as equivalence would be
   dishonest.
4. **ML model trained on SSL Labs output** — could reach high agreement, but
   produces unexplainable grades, needs a large labelled set, and would be
   fitting a black box to a black box. Rejected on explainability and on scope.
5. **No overall grade, only findings** — intellectually honest, but users ask for
   a number and competitors provide one. Rejected on product grounds.

## References

- Benchmark design and corpus: `bench/README.md` (written at M9)
- Standards mapping: `docs/security/standards-mapping.md` (written at M3)
- SSL Labs, *SSL Server Rating Guide* (rating categories and letter grades)
- OWASP, *Risk Rating Methodology*
- [US-02](../product/user-stories.md#us-02--get-a-grade-and-a-prioritised-list)
