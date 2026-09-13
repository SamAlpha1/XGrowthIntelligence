# Fork Setup

Maintainer: **SamAlpha1**  
X: **@samalpha_**

XGrowthIntelligence is designed to run from GitHub Actions without a local environment.

## Required repository configuration

1. Fork `SamAlpha1/XGrowthIntelligence`.
2. Open `Settings -> Secrets and variables -> Actions` in the fork.
3. Under **Secrets**, add `X_BEARER_TOKEN`.
4. Under **Variables**, add `X_USERNAME` without the leading `@`.
5. Optionally add `X_TARGET_KEYWORDS` as a comma-separated variable for niche relevance scoring.
6. Enable GitHub Actions.

The bearer token must remain a Secret. Do not store it as a normal repository variable.

## Available workflows

- **CI** — lint and unit tests.
- **Security Check** — read-only, policy, credential and repository-boundary tests.
- **Upstream Watch** — bounded monitoring of the public recommendation source with semantic diff evidence.
- **Daily Report** — post-processes a successful private metrics artifact into a sanitized job summary.

The live **X Metrics** workflow requires secure Actions Secret mapping before it is activated. Until that wiring exists in the fork, no live account collection is performed.

## Generated runtime data

Runtime files such as `metrics-snapshot.json`, `daily-report.json`, `smart-followers.json`, and `upstream-snapshot.json` are excluded from Git tracking. Private account analytics should remain in GitHub Actions artifacts/job output rather than public commits.

## Rules

- Never place a real token in `.env`, README, issues, logs, source files, or workflow output.
- Keep the X integration read-only.
- Do not add automated follow, like, repost, reply, quote, post, DM, media-upload, or delete behavior to v1.
- Keep user-specific raw analytics out of public commits.
- Keep retries, pagination and workflow execution bounded.

## Fork identity

Fork owners may change account configuration for their own use. The upstream project is maintained by **SamAlpha1 / @samalpha_**.
