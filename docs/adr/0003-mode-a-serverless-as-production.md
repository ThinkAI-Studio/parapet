# 0003. Mode A serverless as production, Mode B as lab

- **Status:** Accepted
- **Date:** 2026-10-26
- **Deciders:** TV1, TV2, TV3

## Context

Parapet must serve real users on a budget of roughly $122 for the whole project,
while two of the three maintainers are studying for AWS SAA-C03 and want
hands-on experience with the services that exam actually tests.

These two goals pull in opposite directions:

- **Serving users** rewards the smallest possible surface: no servers to patch,
  near-zero idle cost, scale-to-zero.
- **Learning AWS** rewards the parts that are expensive and operationally heavy:
  VPC design, subnets, load balancers, autoscaling, multi-AZ databases, caching.
  A serverless stack teaches Lambda and DynamoDB well and teaches almost
  nothing about networking.

A single architecture cannot do both without either over-spending or
under-learning.

## Decision

Run **two separate environments** with a hard boundary between them.

**Mode A — production.** CloudFront → API Gateway → Lambda (Node/TypeScript) →
DynamoDB, with S3 for evidence and public reports, SQS for scan jobs,
EventBridge for schedules and SES for alerts. Deployed with SST. Serves
`parapet.dev`, all real users, and all real scan traffic. Target cost $5/month.

**Mode B — lab.** A private VPC with public/private subnets, ALB, ECS Fargate,
RDS PostgreSQL, ElastiCache Redis, EC2 Spot scan workers and WAF. Built in
Terraform, run in **two bursts of about ten days** (M10 and M11), used to
migrate the scanner, run game days, measure the trade-offs and then
**destroyed**. It never serves real users, never holds the only copy of data,
and is not reachable from Mode A.

The boundary rule: **Mode A never depends on Mode B.** If the lab is torn down,
production is unaffected. Data does not flow from B to A; only lessons and
Terraform modules do.

## Consequences

**Positive**

- Production cost stays near the free tier: ~$5/month instead of ~$150.
- Mode B covers exactly the SAA-C03 domains the serverless stack skips: VPC,
  multi-AZ, load balancing, autoscaling, caching, DR.
- The lab can be broken on purpose without risking users.
- The cost comparison between the two modes becomes a measured artefact
  ([US-11](../product/user-stories.md#us-11--understand-cost-per-scan)) rather
  than an opinion, which is exactly the kind of trade-off question the exam
  asks.
- Two deployments teach Terraform *and* SST, instead of only one.

**Negative**

- Duplicate work: the scanner has to run both as a Lambda and as a container.
- Two sets of IAM, logging and secrets to keep straight.
- Mode B requires disciplined teardown; a forgotten NAT Gateway or RDS instance
  is the most likely way to blow the budget.
- Two weeks of the sixteen go to a system users never touch.

**Neutral**

- Two architectures to document; mitigated by
  `docs/engineering/architecture.md` holding both diagrams.
- The exam does not require Terraform, but writing it is transferable.

## Alternatives considered

1. **Serverless only** — cheapest and simplest, but leaves the VPC, ALB, ECS,
   RDS and multi-AZ material untouched. Two of three members are studying for
   an exam that weights exactly those topics. Rejected as under-serving the
   learning goal.
2. **Containers only (ECS from day one)** — closer to "real" production and
   better for systems learning, but an ALB plus a NAT Gateway alone is ~$50/month
   before any compute. Four months of that exceeds the budget. Rejected on cost.
3. **ECS Fargate with no database, DynamoDB from containers** — cheaper, but
   removes the RDS and caching lessons that motivate Mode B in the first place.
   Rejected as the worst of both.
4. **Kubernetes (EKS)** — maximum learning, minimum budget discipline; a control
   plane is $73/month. Rejected on cost and on time.

## References

- [Scope and budget](../plan/scope.md#budget)
- [Roadmap M10–M11](../plan/roadmap.md)
- [SAA learning plan](../team/learning-plan.md)
