## Summary

<!-- What changed and why. One or two sentences. -->

## Type of change

- [ ] `feat` — new behaviour
- [ ] `fix` — bug fix
- [ ] `docs` — documentation only
- [ ] `infra` — Terraform / AWS / CI
- [ ] `chore` — tooling, dependencies, refactor
- [ ] `security` — hardening, dependency CVE

## Related

<!-- Link the issue and the milestone, e.g. Closes #12 (M3) -->

Closes #

## How was this tested?

<!-- Commands run, or why testing is not applicable. -->

```bash
make check
```

## Checklist

- [ ] Tests added or updated, or the reason explained above
- [ ] Documentation updated if behaviour changed
- [ ] New security checks include a standard mapping in the check catalog
- [ ] No secrets, tokens, AWS account IDs or private hostnames added
- [ ] No new network egress beyond ports 80, 443 and 53
- [ ] Does not add exploitation behaviour (see ADR-0007)
- [ ] CODEOWNERS reviewed

## Risk and rollback

<!-- What could break, and how do we undo it? -->
