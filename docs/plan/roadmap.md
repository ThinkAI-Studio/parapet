# Roadmap

16 weeks. One milestone per week except M1 (two weeks). Updated every Monday.

## Milestones

| Week | ID | Milestone | Exit criteria |
| --- | --- | --- | --- |
| 1 | M0 | Foundations | Docs committed; check catalog with standard mapping; threat model v0; AWS account, budget and tagging in place |
| 2–3 | M1 | Serverless end-to-end | Verified domain → scan → report, running on AWS, deployed by CI with OIDC |
| 4 | M2 | Consent and isolation | DNS TXT verification, SSRF guard, rate limits, terms published; unverified scans impossible |
| 5 | M3 | Full check catalog | 30 checks implemented, rating engine v1, regression fixtures |
| 6 | M4 | Safe active probes | 10 probes implemented and rate limited; no state-changing requests |
| 7 | M5 | GitHub App | Repo ↔ domain linking, Check Runs on deploy, commit stored on scan |
| 8 | M6 | Continuous monitoring | Schedules, history, diff, drift alerts, one alert channel live |
| 9 | M7 | Attack Range, part 1 | 4 scenarios running with browser demos |
| 10 | M8 | Attack Range, part 2 | 8 scenarios, verify-after-fix loop, telemetry |
| 11 | M9 | Benchmark | 120-domain corpus compared with SSL Labs; confusion matrix published |
| 12 | M10 | AWS lab, burst 1 | Terraform VPC/ALB/ECS/RDS; scanner migrated; game day 1 written up |
| 13 | M11 | AWS lab, burst 2 | Multi-AZ, DR drill, cost model, lab destroyed |
| 14 | M12 | Observability and review | OTel traces, dashboards, 3 alerts with runbooks, security review |
| 15 | M13 | Launch | Public report and badge live, waitlist invited, announcement posted |
| 16 | Buffer | Stabilise | Fixes, final benchmark, demo video, mock exam #2 |

## Dependency chain

```
M0 ─> M1 ─> M2 ─> M3 ─> M4
                      ├─> M5 ─> M6 ─> M9
                      └─> M7 ─> M8 ─> M9
M6 ─> M10 ─> M11 ─> M12 ─> M13
M9 ─> M13 (benchmark is published with launch)
```

The critical path is M2 → M3 → M9. Consent and the check catalog cannot slip.

## Gate rule

At the end of a milestone:

- **Met** → proceed.
- **Partially met** → cut from the bottom of the list in
  [scope.md](scope.md#gate-rule), proceed.
- **Not met and on the critical path** → stop, re-plan the remaining weeks, and
  tell each other within the same week.

Deadlines do not move. Scope does.

## Parallel SAA study

Milestones and study are aligned intentionally: the AWS topic of each week is
the one the milestone forces you to use. See
[learning-plan.md](../team/learning-plan.md).

| Checkpoint | Week | Target |
| --- | --- | --- |
| Practice exam #1 | 8 | ≥ 70% |
| Practice exam #2 | 16 | ≥ 80% |
| SAA-C03 exam | 17–18 | Pass (720/1000) |

## What is intentionally not scheduled

No marketing, no conference talks, no paid acquisition, no design system. The
landing page is one page and stays one page until launch.
