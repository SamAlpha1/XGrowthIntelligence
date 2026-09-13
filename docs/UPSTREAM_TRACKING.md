# Upstream Tracking

Maintainer: **SamAlpha1** · X: **@samalpha_**

The project tracks the public X recommendation source repository and records the exact commit SHA used for each evidence snapshot.

## Tracked areas

- Phoenix
- Home Mixer
- `home-mixer/params/param.rs`
- VMRanker
- Grox/content-understanding paths
- Visibility Filtering
- UserCred
- Under-the-Hood reporting paths

## Evidence rule

A changed file is only proof that the file changed. It is not automatically evidence that a ranking weight, account boost, or engagement coefficient changed.

Any future numeric extraction must include:

- source path
- commit SHA
- extraction timestamp
- exact parsed value
- evidence/confidence label

## Workflow

`.github/workflows/upstream-watch.yml` runs on a bounded schedule and stores `upstream-snapshot.json` as a temporary Actions artifact rather than committing generated data to the public repository.
