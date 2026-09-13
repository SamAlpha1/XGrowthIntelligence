from xgrowth.upstream.diff_parser import classify_paths, meaningful_categories
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
