# XGrowthIntelligence

Read-only growth intelligence for X accounts, designed to run entirely with GitHub Actions and the official X API.

**Owner / Maintainer:** [SamAlpha1](https://github.com/SamAlpha1)  
**X:** [@samalpha_](https://x.com/samalpha_)

## Goals

- Track account and post performance without write automation.
- Rank high-value accounts and followers with explainable project heuristics.
- Detect meaningful recommendation-system drift from the public upstream source.
- Produce actionable daily recommendations for manual engagement.
- Stay fork-friendly: no local install, Docker, WSL, or VPS required.

## Safety boundary

Version 1 is strictly read-only toward X. It must never create posts, replies, quotes, reposts, likes, follows, DMs, media uploads, or deletions.

Credentials are read only from GitHub Actions secrets/variables and must never be committed or printed.

## Quick setup

1. Fork this repository.
2. Open `Settings -> Secrets and variables -> Actions`.
3. Add secret `X_BEARER_TOKEN`.
4. Add variable or secret `X_USERNAME`.
5. Enable GitHub Actions.
6. Run the `X Metrics` workflow.
7. Read the job summary and download private artifacts when present.

## Upstream tracking

The project watches the public X recommendation source at `xai-org/x-algorithm`, records commit evidence, and treats project scoring heuristics separately from upstream ranking parameters.

## Project rules

- No automated engagement.
- No cookies, sessions, passwords, or browser login automation.
- No mass-follow, reply spam, fake impressions, or fake engagement.
- No user-specific raw analytics committed to the public repository by default.
- All retries are bounded and workflows are designed to be idempotent.
- Every upstream-derived signal must retain source path and commit SHA.

## Status

Bootstrap in progress. The repository is being built in phases with CI and safety checks enabled from the start.

---

Built and maintained by **SamAlpha1** — X: **@samalpha_**
