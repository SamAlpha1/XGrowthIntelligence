# Architecture

Owner: **SamAlpha1** · X: **@samalpha_**

## Flow

1. **Upstream Watcher** reads the current public recommendation source commit and relevant changed paths.
2. **Diff Parser / Signal Extractor** turns source changes into evidence records without inventing ranking weights.
3. **Read-Only X Client** collects permitted account and post data through official read endpoints.
4. **Scoring Layer** ranks accounts and followers with clearly labeled project heuristics.
5. **Reporting Layer** writes sanitized summaries and private workflow artifacts.
6. **Safety Layer** blocks write methods/scopes and protects credentials.

## Separation of evidence

Upstream-derived evidence and project scoring heuristics are separate data domains. A changed upstream path is not treated as proof that a ranking weight changed. Any future extraction of numeric parameters must retain source path, commit SHA, timestamp, and evidence level.

## Runtime

The supported deployment target is GitHub Actions. Workflows must have finite timeouts, bounded retries, least-privilege permissions, and no dependency on local machines.
