# Safety Boundary

Maintainer: **SamAlpha1** · X: **@samalpha_**

Version 1 is intentionally read-only toward X.

## Allowed

- Read public account data that the configured official API access permits.
- Read public post data and permitted public metrics.
- Analyze locally inside the GitHub Actions runner.
- Produce job summaries and private artifacts.

## Forbidden in v1

- Creating, editing, or deleting posts.
- Follow or unfollow actions.
- Likes, unlikes, reposts, quotes, or replies.
- DMs or media uploads.
- Cookie/session/password login automation.
- Fake impressions, fake engagement, mass-following, or reply spam.

## Enforcement

`src/xgrowth/safety/readonly_guard.py` allows only read HTTP methods to approved X API hosts and rejects known write scopes. CI and the dedicated Security Check run tests for this boundary.

Credentials must remain in GitHub Actions secrets and must never be committed or printed.
