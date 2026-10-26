# 0004. DynamoDB over RDS for Mode A

- **Status:** Amended by [ADR-0011](0011-zero-spend-mode-a.md)
  (Capacity mode changed from on-demand to provisioned 25 RCU / 25 WCU for zero-spend.)
- **Date:** 2026-10-26
- **Deciders:** TV1, TV2, TV3

## Context

Mode A needs to store four kinds of data:

1. **Accounts and verified domains** — small, read-heavy, strongly consistent
   when a scan is about to be dispatched.
2. **Scans and findings** — append-only, growing by roughly 10,000 scans over
   sixteen weeks, each with 30 check results.
3. **Grade history** — one row per scan per domain, read for trends and diffing.
4. **Public report metadata** — keyed by an unguessable identifier.

Access patterns are known up front and narrow: get a domain by ID, list scans
for a domain in reverse chronological order, get a scan with its findings, get
the latest scan for a domain, list domains for an account. There are no ad-hoc
joins, no reporting queries over arbitrary dimensions, and no transactions
spanning more than two items.

Constraints: production must stay near $5/month, the team is three people with
no DBA, and Mode A has no VPC, so a managed relational database would force one
into existence.

## Decision

Mode A uses **DynamoDB**, single-table design, on-demand capacity, with two
global secondary indexes for the reverse-chronological access patterns.

Primary key design:

| Entity | PK | SK |
| --- | --- | --- |
| Account | `ACCOUNT#<id>` | `ACCOUNT#<id>` |
| Domain | `ACCOUNT#<id>` | `DOMAIN#<domain>` |
| Scan | `DOMAIN#<domain>` | `SCAN#<timestamp>#<id>` |
| Finding | `SCAN#<scan-id>` | `FINDING#<check-id>` |
| Verification | `DOMAIN#<domain>` | `VERIFY#<timestamp>` |

GSI-1 (`GSI1PK`/`GSI1SK`) serves "latest scan per domain" and public report
lookup by public ID. GSI-2 serves "scans by repository and commit" for the
GitHub App story (US-07). TTL is used for raw evidence pointers and abuse logs
(90-day retention).

RDS is still used — in Mode B, where it is a learning objective, not a
production dependency.

## Consequences

**Positive**

- No idle cost: on-demand billing means a quiet week costs cents.
- No VPC, no connection pool, no migrations, no patching, no failover drill
  required for a service with no SLA.
- Every access pattern is a documented query, which forces the data model to be
  designed rather than discovered.
- Scales to the 10,000-scan target without any capacity planning.
- It is a core SAA-C03 topic (partition keys, GSI, capacity modes, hot
  partitions), so the choice is also study material.

**Negative**

- Single-table design is harder to explain and to change than a normalised
  schema; onboarding a new contributor costs more.
- No ad-hoc SQL. Any future analytics need export to S3 and Athena.
- Cannot do cross-entity transactions beyond two items without extra care;
  domain verification and scan dispatch are therefore ordered by the queue, not
  by a transaction.
- The team must learn partition-key design to avoid hot partitions on the
  `DOMAIN#` prefix — the busiest domains are the hottest keys. Mitigated by
  sharding scan writes if a single domain exceeds ~1,000 writes/second, which
  the target load never approaches.

**Neutral**

- Local development uses DynamoDB Local in Docker Compose; the query code is the
  same.
- Mode B's RDS becomes a deliberate comparison, not a replacement.

## Alternatives considered

1. **RDS PostgreSQL (Mode A)** — familiar, flexible, one schema. Rejected: it
   requires a VPC and a NAT Gateway in Mode A (~$35–50/month before the
   instance), plus connection management from Lambda. It consumes the entire
   budget to buy flexibility the access patterns do not need.
2. **Aurora Serverless v2** — scales down, but not to zero in a meaningful way
   for this workload, and the VPC requirement is unchanged. Rejected on cost.
3. **SQLite on S3 / Litestream** — cheap and simple for reads, but write
   concurrency from multiple Lambda invocations is a real problem, and the
   durability story is worse than the problem deserves. Rejected.
4. **Postgres on a single small EC2 instance** — cheapest relational option, but
   reintroduces server patching, backups and single-point-of-failure management
   to a team with no on-call. Rejected.

## References

- Data model design (M1): `docs/engineering/data-model.md`
- AWS, *DynamoDB single-table design* — Rick Houlihan's re:Invent talks
- [US-02](../product/user-stories.md#us-02--get-a-grade-and-a-prioritised-list),
  [US-07](../product/user-stories.md#us-07--see-which-commit-changed-the-grade)
