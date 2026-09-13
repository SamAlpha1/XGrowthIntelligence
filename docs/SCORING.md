# Scoring

Owner: **SamAlpha1** · X: **@samalpha_**

XGrowthIntelligence keeps project scoring separate from upstream X recommendation parameters.

## Smart Follower components

The project schema can use relevance, authority, verification, recency, engagement quality, network value, conversion likelihood, and a risk penalty. These are internal prioritization heuristics for manual review.

If evidence for a component is unavailable, partial scoring excludes that component instead of filling it with an invented value. Each result reports `evidence_coverage` and `missing_features`.

## Evidence sources

Current read-only follower profile evidence can include public follower/following/post/listed counts, verification state/type, public profile text, and configured target keywords. Features requiring unavailable evidence remain missing.

## Rule

No project score is presented as an upstream ranking formula, ranking weight, or guaranteed growth signal.
