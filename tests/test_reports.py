from xgrowth.reporting.daily_report import build_daily_report
from xgrowth.reporting.github_summary import render_daily_summary


def test_daily_report_is_read_only_and_signed() -> None:
    account = {
        "username": "samalpha_",
        "verified": True,
        "verified_type": "blue",
        "public_metrics": {"followers_count": 100, "following_count": 20, "tweet_count": 30},
    }
    posts = [
        {
            "id": "1",
            "public_metrics": {
                "impression_count": 1000,
                "reply_count": 10,
                "retweet_count": 5,
                "quote_count": 2,
            },
        }
    ]
    report = build_daily_report(account, posts)
    assert report["owner"] == "SamAlpha1"
    assert report["x_handle"] == "samalpha_"
    assert report["safety"]["x_write_actions"] == 0
    assert report["manual_recommendations"][0]["action_mode"] == "manual_only"
    summary = render_daily_summary(report)
    assert "SamAlpha1" in summary
    assert "@samalpha_" in summary
    assert "No X write action" in summary
