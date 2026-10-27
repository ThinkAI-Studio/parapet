# 0011. Zero-spend architecture for Mode A

- **Status:** Accepted
- **Date:** 2026-10-26
- **Deciders:** project owner

## Context

The initial architecture for Parapet (recorded in [ADR-0003](0003-mode-a-serverless-as-production.md),
[ADR-0004](0004-dynamodb-over-rds.md), and [ADR-0009](0009-landing-page-hosting.md)) assumed an estimated
budget of ~$122 across 16 weeks (~$20 for Mode A serverless, ~$90 for two Mode B lab bursts, and $12 for a domain).

That baseline no longer holds. A strict zero-spend requirement has been established: production must run
at $0/month indefinitely inside always-free allowances. Several services in the original plan violate this
constraint:
- AWS WAF costs $5/month per web ACL plus $1/rule.
- Route53 hosted zones cost $0.50/month each.
- AWS HTTP API (API Gateway) is only free for the first 12 months (1M calls/month), then $1.00/M.
- Amazon SES eliminated its free tier for new AWS accounts created after 2026-07-21.
- Amazon S3 free tier (5 GB, standard requests) expires after 12 months, and egress incurs transfer costs.
- Secrets Manager costs $0.40/secret/month and KMS customer managed keys cost $1.00/key/month.
- DynamoDB on-demand charges per request once free credits lapse, whereas provisioned capacity includes an
  always-free tier of 25 RCU and 25 WCU.
- Mode B lab bursts (~$4.50/day for NAT gateway, ALB, RDS, and ECS) cannot be reconciled with zero-spend.

To maintain Parapet as an open, accessible project without recurring infrastructure costs, the production
architecture is realigned to an always-free baseline combining Cloudflare and AWS.

## Decision

Realign the Mode A architecture to a verified zero-spend baseline, and defer the Mode B lab outside the
16-week project scope and budget.

| Area | Before (ADR-0003/0004/0009) | Now | Why |
| --- | --- | --- | --- |
| Edge, TLS, DNS, WAF | CloudFront + WAF + Route53 | Cloudflare free (DNS already there, WAF custom rules, 1 rate-limit rule) | WAF $5/mo and hosted zone $0.50/mo break zero-spend |
| API entry | API Gateway | Lambda Function URL behind Cloudflare with a shared secret header | HTTP API free only 12 months, then $1/M |
| Alerts | SES | Telegram webhook | SES has no free tier for new accounts since 2026-07-21 |
| Evidence | S3 | Cloudflare R2, private bucket, presigned URLs, 90-day lifecycle | S3 free tier ends after 12 months; R2 has 10 GB and free egress |
| Data capacity | DynamoDB on-demand | DynamoDB provisioned 25 RCU / 25 WCU + reserved concurrency on the worker; on-demand documented as fallback | always-free covers provisioned only |
| Secrets | Secrets Manager / KMS CMK | SSM Parameter Store SecureString standard | $0.40/secret and $1/key |
| IaC | SST | Terraform | learning goal; provider coverage |
| Landing | Vercel, then S3+CloudFront at M15 | Cloudflare Pages at parapet.thinkai.id.vn from day one | unlimited static requests; no commercial-use ambiguity |
| App host | api.parapet.dev | app.parapet.thinkai.id.vn, API under /api/* | cookie isolation from the studio portfolio at the apex |
| Auth | none specified | Cognito User Pool, Essentials tier (10k MAU free), built-in email sender (~50/day) | stays inside free tier; no hand-rolled auth |
| CI/CD | GitHub Actions + OIDC (unchanged) | same, plus Terraform apply in CI | no long-lived keys |
| SMTP STARTTLS probe | one of the 10 probes in Mode A | moved to Mode B only; Mode A ships 9 of 10 | Lambda cannot reach outbound port 25 without a VPC and an AWS request |
| Mode B lab | M10–M11 bursts | deferred to a future roadmap, outside the 16-week scope and budget | ~$4.50/day is not zero-spend |

## Consequences

**Positive**

- True $0/month baseline: production runs permanently inside always-free allowances across Cloudflare and AWS.
- Cloudflare provides unlimited static requests, DDoS mitigation, custom WAF rules, and free TLS.
- Cloudflare R2 provides 10 GB of storage with zero egress fees, removing bandwidth cost risk for public reports and scan evidence.
- Terraform provides a unified, cross-provider IaC toolchain for both Cloudflare and AWS resources.
- Cognito User Pool Essentials tier provides managed authentication for up to 10,000 MAU without custom auth maintenance or third-party subscription costs.
- Telegram webhook alerts deliver instant notifications without SES sandbox limitations or email deliverability headaches.

**Negative**

- Two control planes: operational and security configuration is split across Cloudflare (DNS, WAF, Pages, R2) and AWS (Lambda, DynamoDB, SQS, Cognito, SSM).
- DynamoDB throttle risk: provisioned capacity is capped at 25 RCU / 25 WCU. Bursts must be buffered by SQS and reserved worker concurrency to avoid throttling.
- No access logs: neither Cloudflare Free nor CloudFront Free provides edge access logs without paid plans.
- Terraform state storage is not free long-term: state is kept locally initially; migrating to an S3 backend after AWS's 12-month free tier costs small cents for storage and API calls.
- Cognito built-in email sender is capped around ~50 emails/day, which constrains registration velocity during peak user influxes.
- Mode B learning goal is deferred: hands-on practice with AWS VPC, ALB, and RDS cannot occur in live AWS bursts and must come from LocalStack or a future lab roadmap.
- The SMTP STARTTLS probe cannot run in Mode A: AWS Lambda blocks outbound traffic on port 25 without an explicit VPC and AWS support request, so Mode A ships 9 of the 10 planned active probes.

**Neutral**

- Deployments continue via GitHub Actions using OIDC, eliminating long-lived credentials.
- Application routing uses `app.parapet.thinkai.id.vn` with `/api/*` proxied to the Lambda Function URL, providing cookie isolation from the apex domain portfolio.
- DynamoDB on-demand remains documented as an emergency fallback if provisioned capacity cannot handle sustained traffic.

## Alternatives considered

1. **CloudFront flat-rate Free** (1M requests, 1 domain, 5 cache behaviours, no access logs) — Rejected: 1M requests/month cap, 1 domain, 5 cache behaviours, 5 WAF rules, and no access logs without Pro.
2. **API Gateway HTTP API** — Rejected: The free tier lasts only 12 months (1M calls/month), after which it costs $1.00/M requests. Lambda Function URLs provide a permanent always-free HTTPS entry point.
3. **SES and SNS email** — Rejected: Amazon SES has no free tier for accounts created after 2026-07-21, costing $0.10/1,000 emails plus data transfer. Telegram webhook alerts are free, instant, and reliable.
4. **S3 with lifecycle** — Rejected: Amazon S3 free tier expires after 12 months, and egress bandwidth is billed. Cloudflare R2 provides 10 GB always-free storage with $0 data egress.
5. **Secrets Manager** — Rejected: Charges $0.40/secret/month and $1.00/month per KMS CMK. AWS SSM Parameter Store standard SecureString parameters are always free.
6. **SST** — Rejected: SST couples the deployment to AWS-centric abstractions and lacks first-class multi-provider orchestration for Cloudflare DNS/WAF/Pages/R2. Terraform covers both providers natively.
7. **Vercel Hobby** — Rejected: Terms of service prohibit commercial use, creating policy ambiguity. Cloudflare Pages offers unlimited requests and clear terms at $0.
8. **Hand-rolled auth** — Rejected: Storing password hashes and rolling custom session tokens creates substantial security risks and maintenance overhead.
9. **Auth0 free tier** — Rejected: Third-party dependency with vendor lock-in and severe pricing cliffs above free limits. Amazon Cognito Essentials provides 10,000 MAU always-free inside AWS.

## References

- [ADR-0003: Mode A serverless as production](0003-mode-a-serverless-as-production.md)
- [ADR-0004: DynamoDB over RDS for Mode A](0004-dynamodb-over-rds.md)
- [ADR-0009: Landing page hosting](0009-landing-page-hosting.md)
- [Scope and budget](../plan/scope.md#budget)
- [Roadmap](../plan/roadmap.md)
- [Threat model](../security/threat-model.md)
- AWS Free Tier: Lambda, DynamoDB, SQS, SSM Parameter Store, Cognito
- Cloudflare Free Tier and Cloudflare R2 pricing
