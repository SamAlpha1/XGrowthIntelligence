# XGrowthIntelligence

Read-only growth intelligence for X accounts, designed for GitHub Actions and the official X API.

**Owner / Maintainer:** [SamAlpha1](https://github.com/SamAlpha1)  
**X:** [@samalpha_](https://x.com/samalpha_)

## Goals

- Track account and post performance without write automation.
- Rank high-value accounts and followers with explainable project heuristics.
- Detect meaningful recommendation-system drift from the public upstream source.
- Produce actionable recommendations for manual engagement.
- Stay fork-friendly: no local install, Docker, WSL, or VPS required.

## Safety boundary

Version 1 is strictly read-only toward X. It must never create posts, replies, quotes, reposts, likes, follows, DMs, media uploads, or deletions.

Credentials belong only in GitHub Actions Secrets and must never be committed or printed. Runtime analytics are generated as workflow outputs/artifacts and are gitignored by default.

## Current status

- **CI:** operational and passing.
- **Security Check:** operational and passing.
- **Upstream Watch:** operational and passing on an hourly bounded schedule.
- **Semantic drift detection:** operational; metadata/comment-only changes are separated from source changes.
- **Read-only X client:** implemented with bounded retries and write-method/scope guards.
- **Smart follower/account ranking:** implemented with explicit evidence coverage and no missing-feature imputation.
- **Impression / engagement / conversion / anomaly engines:** implemented.
- **Strategy engine:** manual recommendations only.
- **Daily report engine and post-processor workflow:** implemented.
- **X Metrics runtime workflow:** secure repository-secret wiring remains to be activated before live account collection.

## Upstream tracking

The project watches the public X recommendation source at `xai-org/x-algorithm`, records exact commit/path evidence, and treats project scoring heuristics separately from upstream ranking parameters.

A changed file is not automatically treated as a ranking change. The watcher classifies source patches and can exclude non-semantic changes such as mirrored configuration sync timestamps.

## Fork setup

See [`docs/FORK_SETUP.md`](docs/FORK_SETUP.md). The intended runtime requires only GitHub Actions configuration:

- `X_BEARER_TOKEN` as a GitHub Actions **Secret**.
- `X_USERNAME` as a GitHub Actions **Variable**.
- Optional `X_TARGET_KEYWORDS` for niche relevance scoring.

Do not put the bearer token in source files, variables, issues, logs, or workflow output.

## Project rules

- No automated engagement.
- No cookies, sessions, passwords, or browser login automation.
- No mass-follow, reply spam, fake impressions, or fake engagement.
- No user-specific raw analytics committed to the public repository by default.
- All retries and workflow runs are bounded.
- Every upstream-derived signal retains source path and commit SHA.
- Internal scoring remains clearly separated from upstream ranking evidence.

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/SAFETY.md`](docs/SAFETY.md)
- [`docs/SCORING.md`](docs/SCORING.md)
- [`docs/UPSTREAM_TRACKING.md`](docs/UPSTREAM_TRACKING.md)
- [`docs/FORK_SETUP.md`](docs/FORK_SETUP.md)
- [`CHANGELOG.md`](CHANGELOG.md)

---

Built and maintained by **SamAlpha1** — X: **@samalpha_**
