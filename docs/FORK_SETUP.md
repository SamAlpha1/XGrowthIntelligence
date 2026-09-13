# Fork Setup

Maintainer: **SamAlpha1**  
X: **@samalpha_**

XGrowthIntelligence is designed to run from GitHub Actions without a local environment.

## Setup

1. Fork `SamAlpha1/XGrowthIntelligence`.
2. Open the fork's `Settings -> Secrets and variables -> Actions`.
3. Add `X_BEARER_TOKEN` as an Actions secret.
4. Add `X_USERNAME` as an Actions variable or secret, depending on the workflow version in your fork.
5. Enable Actions for the fork.
6. Run the available read-only workflows.
7. Read job summaries and private artifacts from the Actions run.

## Rules

- Never place a real token in `.env`, README, issues, logs, workflow output, or committed files.
- Keep the X integration read-only.
- Do not add automated follow, like, repost, reply, quote, post, DM, media-upload, or delete behavior to v1.
- Keep user-specific raw analytics out of public commits.

## Fork identity

Fork owners may change account configuration for their own use. The upstream project is maintained by **SamAlpha1 / @samalpha_**.
