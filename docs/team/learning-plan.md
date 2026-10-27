# Learning Plan — AWS SAA-C03

TV2 and TV3 sit the **AWS Certified Solutions Architect – Associate (SAA-C03)**
exam in **weeks 17–18**, after the project ships. TV1 uses the same weekly
structure for full-stack depth and reviews the AWS design sessions.

**Budget: 5 hours per week, per person, on top of 8–10 hours of project work.**
That is ~80 hours before the exam. It is enough only if the study is aimed at
the exam and the project does the practising.

The core idea: **do not study AWS in the abstract.** Each week's project
milestone forces the use of specific services; study the theory behind exactly
those services, then write the ADR that explains the trade-off. The exam rewards
people who have made the decision, not people who have memorised a service list.

## Weekly rhythm

| Slot | Time | What |
| --- | --- | --- |
| Mon | 30 min | Read the week's exam domain in the official exam guide; write three questions you cannot answer |
| Wed | 90 min | Hands-on in the personal AWS account, inside the week's milestone work |
| Sat | 120 min | Practice questions for the week's domain; log every wrong answer |
| Sun | 60 min | Design review with the other member (see [team.md](../plan/team.md#review-pairing-for-saa)); write the ADR |

Rules:

- Hands-on happens in the **personal account with a budget alarm**, never in
  production.
- Every practice question answered wrong goes into a single `saa-wrong.md` file
  (private, not committed) with the *reason* — "guessed", "misread", "didn't
  know the service".
- Sunday's design review is not optional; it is the study method.
- If a week is lost, drop the practice questions, not the hands-on.

## Milestone → exam domain map

The official SAA-C03 domains, weighted: **Secure architectures 30%**,
**Resilient architectures 26%**, **High-performing architectures 24%**,
**Cost-optimised architectures 20%**.

| Week | Milestone | AWS topics it forces | Exam domain | Study focus |
| --- | --- | --- | --- | --- |
| 1 | M0 Foundations | Accounts, IAM users/roles, budgets, tagging, regions | Secure 1.1–1.2 | IAM policy evaluation, root vs. role, budget alarms |
| 2–3 | M1 Serverless end-to-end | Lambda, Function URLs, DynamoDB, SSM, OIDC | Performant 3.1, Secure 1.4 | Lambda limits and cold starts, DynamoDB provisioned capacity, Function URL security |
| 4 | M2 Consent and isolation | Route53, ACM, WAF, VPC endpoints, Secrets Manager | Secure 1.3–1.5 | DNS record types, certificate validation, least privilege |
| 5 | M3 Full check catalog | S3 lifecycle and storage classes, DynamoDB indexes | Cost 4.1, Performant 3.4 | Storage class trade-offs, GSI vs. LSI, hot partitions |
| 6 | M4 Safe active probes | Lambda concurrency, SQS, DLQ, throttling | Resilient 2.2, Performant 3.3 | Decoupling, visibility timeout, backoff and retry |
| 7 | M5 GitHub App | Cognito auth, SSM Parameter Store SecureString, IAM | Secure 1.4–1.6 | Parameter Store vs. Secrets Manager, least privilege, IAM policies |
| 8 | M6 Continuous monitoring + **practice exam #1** | EventBridge, CloudWatch, alarms, notifications | Resilient 2.3, Cost 4.1 | Event-driven patterns, metrics vs. logs, alarm design |
| 9 | M7 Range part 1 | Isolated network, security groups, egress control | Secure 1.3, 1.5 | SG vs. NACL, subnet design, VPC flow logs |
| 10 | M8 Range part 2 + verify loop | S3 static hosting, presigned URLs, CloudFront behaviours | Secure 1.4, Performant 3.2 | Cache behaviours, signed URLs vs. cookies, TTLs |
| 11 | M9 Benchmark | Batch, Step Functions, cost of egress | Performant 3.1, Cost 4.2 | Orchestration choice, data transfer pricing |
| 12 | M10 Lab burst 1 (deferred) | **VPC, subnets, IGW/NAT, ALB, ECS Fargate, RDS** (LocalStack/theory) | Resilient 2.1, Performant 3.2 | Multi-AZ vs. read replica, target groups, health checks, Fargate vs. EC2 |
| 13 | M11 Lab burst 2 (deferred) | Multi-AZ, ElastiCache, Route53 failover, backup and DR (LocalStack/theory) | Resilient 2.1–2.3, Cost 4.3 | RTO/RPO, pilot light vs. warm standby, cache strategies |
| 14 | M12 Observability and review | CloudWatch dashboards, X-Ray/OTel, Config, GuardDuty | Secure 1.6, Resilient 2.3 | Detection vs. prevention, compliance tooling |
| 15 | M13 Launch | AWS budgets, zero-spend monitoring, pricing models | Cost 4.1–4.3 | Pricing model per service, free-tier boundaries |
| 16 | Buffer + **practice exam #2** | Review weak domains only | All | Timed exam conditions, 130 minutes |
| 17–18 | **SAA-C03 exam** | — | — | Light review; no new material |

Weeks 12–13 cover the topics Lambda cannot teach: VPC routing, load balancing,
multi-AZ databases and DR. Because the live AWS Mode B lab is deferred under
zero-spend ([ADR-0011](../adr/0011-zero-spend-mode-a.md)), hands-on practice for
these services uses LocalStack and practice environments rather than live AWS bursts.

## Checkpoints

| Checkpoint | Week | Target | If missed |
| --- | --- | --- | --- |
| Practice exam #1 (full, timed) | 8 | ≥ 70% | Identify the two weakest domains; spend 2 h/week on them for four weeks; retake at week 12 |
| Practice exam #2 (full, timed) | 16 | ≥ 80% | Move the exam slot to weeks 19–20; the project is finished by then |
| Real exam | 17–18 | Pass (720/1000) | Re-book once, after two weeks of targeted study |

Book the exam **at week 12**, not at week 16. A booked date is the only reliable
forcing function.

## Resources (deliberately short)

| Resource | Use | Time |
| --- | --- | --- |
| Official SAA-C03 Exam Guide | Domain weights and task statements | 1 h, once |
| AWS Skill Builder exam prep | Structured coverage, free | 8–10 h total |
| AWS documentation | Only the page for the service in front of you | As needed |
| One practice-exam set (~500 questions) | Timed practice, and the wrong-answer log | 6–8 h total |
| This project's ADRs | Trade-off reasoning in our own words | Continuous |

One resource per purpose. Collecting courses is a way of avoiding the exam.

## What the project deliberately does *not* teach

Be honest about the gap and cover it with focused reading:

| Gap | Covered by |
| --- | --- |
| Multi-account governance (Organizations, SCPs) | Read + one page of notes, week 14 |
| Hybrid networking (Direct Connect, Transit Gateway, VPN) | Read + exam questions, week 13 |
| Migration services (DMS, Snowball, DataSync) | Read only, week 15 |
| Analytics (Kinesis, Glue, Athena, Redshift) | Exam questions only; out of scope for the product |
| Machine learning services | Exam questions only |
| Enterprise DR contracts | The Mode B DR drill covers the concepts at small scale |

## Tracking

Weekly, in the Monday sync, two lines each:

```
SAA: domain 2 practice 18/25 — weak on SQS visibility timeout
Project: M6 alert dedupe done; Telegram webhook alerts live
```

No dashboards, no streaks, no app. If the two lines stop appearing, the plan has
failed and we say so in the same week.

## After the exam

- Phase 2 (AI triage and remediation PR) starts only after the exam result.
- The learning plan is then replaced by a shorter one aimed at the next goal
  (Security Specialty or the Professional exam), reusing the same weekly shape.
- The ADR habit continues — it is the most durable thing this plan produces.
