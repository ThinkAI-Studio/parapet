# 0009. Landing page on Vercel first, S3 + CloudFront at M15

- **Status:** Accepted
- **Date:** 2026-10-26
- **Deciders:** TV1, TV3

## Context

The landing page is the only thing that exists before the product does, and its
single job in weeks 1–14 is to collect a waitlist so that M15 has real people to
invite. It is one page, it changes weekly, and it must never compete for time
with the scanner.

Two constraints pull against each other:

- **Iteration speed.** During M0–M2 the page changes more often than anything
  else in the repository. A deploy that takes five minutes and requires a
  Terraform plan is a deploy that does not happen.
- **Learning and ownership.** The AWS/SAA goal wants CloudFront, ACM, Route53
  and Origin Access Control touched for real. Deferring them to a "someday"
  means they are never touched, and the product ends up with a hosting
  dependency we cannot explain.

There is also a licence detail: Vercel's Hobby plan is for non-commercial use.
Parapet is MIT and free, so a waitlist page is defensible today — but "free
product with a landing page" is exactly the situation that changes quietly, and
we should not be relying on a plan whose terms we would have to re-read if the
project ever took money.

## Decision

**Phase 1 (M0 → M14): Vercel.** The landing page is a Next.js app in
`apps/landing`, deployed from `master` on Vercel's Hobby plan with preview
deployments for pull requests. Zero infrastructure to maintain, zero cost, and a
deploy per push.

**Phase 2 (M15): S3 + CloudFront.** The same Next.js output is exported
statically and served from a private S3 bucket behind CloudFront with Origin
Access Control, a certificate from ACM in `us-east-1`, and Route53 for
`parapet.dev` and `www`. Vercel is then removed.

The migration is a scheduled deliverable of M15, not an optional cleanup, and it
is deliberately performed *after* the static export is stable.

**The seam that makes the migration cheap:** the waitlist form never calls a
Vercel function. It posts to `https://api.parapet.dev/waitlist` (API Gateway →
Lambda → DynamoDB) from day one. Hosting and application are separate from the
first commit, so moving the page changes DNS and nothing else.

## Consequences

**Positive**

- The landing page costs nothing and needs no pipeline work during the weeks
  when the team is building the scanner.
- Preview deployments give TV1 a URL to share for feedback without a review
  cycle on infrastructure.
- The M15 migration is a real, measured exercise: cache behaviours, invalidation,
  OAC, certificate validation, DNS cutover — all SAA-relevant, all with a
  rollback path (DNS back to Vercel) that takes minutes.
- The waitlist keeps working across the migration because it was never coupled
  to the host.
- It removes the Hobby-plan terms question before it can become a problem.

**Negative**

- Two places to look when the landing page is broken for the next fourteen
  weeks, and a migration that will consume part of M15.
- Static export constrains the page: no server-side rendering, no image
  optimisation service. Acceptable for one page.
- DNS is at Route53 but the apex points at Vercel via records we will have to
  change, so the cutover needs a TTL lowered a day in advance. Written into the
  M15 checklist.
- Someone will ask why the landing page is not on AWS like everything else, and
  the answer is "because it will be at M15" — a temporary inconsistency that has
  to be explained.

**Neutral**

- CI builds the landing page on every pull request; deployment stays on Vercel's
  Git integration until M15, then moves to GitHub Actions with OIDC.
- The domain is registered once and does not move.

## Alternatives considered

1. **S3 + CloudFront from day one** — one architecture, no migration, learns the
   edge services earlier. Rejected: it front-loads the most infrastructure-heavy
   work into the weeks when the product has the least value, and every copy
   change would need a build and an invalidation.
2. **Cloudflare Pages** — free, fast, no commercial-use ambiguity, better
   defaults than Vercel Hobby. Rejected: it is a third platform with no
   relationship to either learning goal, so it trades a temporary dependency for
   a permanent one.
3. **AWS Amplify Hosting** — keeps everything in AWS and supports Next.js. It
   hides exactly the CloudFront, S3 and ACM mechanics we want to learn, at a
   higher cost than the manual setup. Rejected.
4. **Stay on Vercel permanently** — simplest, and honestly fine for one page.
   Rejected because it leaves `parapet.dev` outside the AWS account and leaves
   the Hobby-plan question unresolved.
5. **No landing page until M15** — saves a few hours and loses the only source
   of real users before launch. Rejected.

## References

- [Roadmap M13–M15](../plan/roadmap.md)
- [Team ownership](../plan/team.md)
- [US-10 — publish a report and a badge](../product/user-stories.md#us-10--publish-a-report-and-a-badge)
- Vercel, *Hobby plan fair use* and *Static Exports* documentation
- AWS, *Restricting access to an Amazon S3 origin* (Origin Access Control)
