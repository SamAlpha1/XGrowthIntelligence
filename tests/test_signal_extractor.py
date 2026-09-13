from xgrowth.upstream.diff_parser import classify_paths, meaningful_categories
from xgrowth.upstream.semantic_diff import classify_patch
from xgrowth.upstream.watcher import is_relevant_path


def test_relevant_paths_are_detected() -> None:
    assert is_relevant_path("phoenix/example.rs")
    assert is_relevant_path("home-mixer/params/param.rs")
    assert is_relevant_path("vm-ranker/dpp.rs")
    assert not is_relevant_path("README.md")


def test_changed_path_classification_does_not_infer_weights() -> None:
    signals = classify_paths(["phoenix/example.rs", "vm-ranker/dpp.rs"])
    assert meaningful_categories(signals) == ("phoenix", "vm-ranker")
    assert all(signal.evidence_level == "path-evidence" for signal in signals)


def test_param_sync_timestamp_is_not_meaningful_drift() -> None:
    patch = (
        "@@ -1,4 +1,4 @@\n"
        "-// mirrored from config feature-switch defaults; last sync 2026-09-10T16:21:03Z\n"
        "+// mirrored from config feature-switch defaults; last sync 2026-09-11T16:22:45Z\n"
        " use xai_feature_switches::param;\n"
    )
    result = classify_patch("home-mixer/params/param.rs", patch)
    assert result["classification"] == "sync_metadata_only"
    assert result["meaningful"] is False


def test_non_comment_source_change_is_meaningful_without_claiming_effect() -> None:
    patch = "@@ -1,2 +1,2 @@\n-let old_value = 1;\n+let new_value = 2;\n"
    result = classify_patch("vm-ranker/dpp.rs", patch)
    assert result["classification"] == "source_change"
    assert result["meaningful"] is True
    assert "no ranking effect" in str(result["reason"]).lower()
