## Code Review Rules

Review for precision, not maximum comment volume.

Report only serious defects introduced or worsened by the current diff:
- crashes or broken execution;
- incorrect behavior or corrupted results;
- security vulnerabilities;
- data loss or corruption;
- broken compatibility;
- likely production incidents.

Before posting a comment, prove:

trigger → failure → impact

Every finding must cite the changed line or changed behavior and explain why the issue is caused by this diff.

Do not report:
- style, naming, formatting, or readability;
- optional refactors;
- speculative edge cases;
- hypothetical future requirements;
- test coverage alone;
- minor performance concerns;
- pre-existing issues;
- subjective design preferences;
- multiple comments for the same root cause.

Do not post P2, P3, minor, or nit-level findings.

If no serious defect is proven, post no inline comments and approve the review.
