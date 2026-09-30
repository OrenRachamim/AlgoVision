import datetime as dt

from algovision.data import newsfeed as N
from algovision import sentiment as S

RSS = """<?xml version="1.0"?><rss version="2.0"><channel><title>x</title>
<item><title>Nike forecasts surprise sales drop as China weakness hurts turnaround - Reuters</title>
<link>https://example.com/a</link><pubDate>Wed, 01 Apr 2026 21:10:00 GMT</pubDate><source url="https://reuters.com">Reuters</source></item>
<item><title>Nike Can&amp;#39;t Fix Its China Problem</title><link>https://example.com/b</link>
<pubDate>Thu, 02 Apr 2026 09:00:00 GMT</pubDate><source url="https://wsj.com">WSJ</source></item>
<item><title>no date</title><link>x</link></item>
</channel></rss>"""


def test_parse_google_rss_and_query():
    items = N.parse_google_rss(RSS)
    assert [x["date"] for x in items] == ["2026-04-01", "2026-04-02"]
    assert items[0]["title"] == "Nike forecasts surprise sales drop as China weakness hurts turnaround" and items[0]["publisher"] == "Reuters"
    assert items[1]["title"] == "Nike Can't Fix Its China Problem"
    assert N.parse_google_rss("not xml") == []
    assert N.company_query("NCLH", "Norwegian Cruise Line Holdings Ltd.") == '"Norwegian Cruise"'
    assert N.company_query("NKE", "NIKE, Inc.") == '"NIKE"' and N.company_query("ABC", "") == '"ABC"'


def test_google_news_offline_and_cached(tmp_path):
    assert N.google_news("q", tmp_path, offline=True) == []
    p = N._cache_path(tmp_path, "news", "q")
    p.write_text('[{"date": "2026-01-01", "title": "t", "publisher": "", "summary": "", "link": "", "source": "google"}]')
    assert N.google_news("q", tmp_path, offline=True)[0]["title"] == "t"
    assert N.stocktwits("X", tmp_path, offline=True) == {}


def _h(date, title, pub="Wire"):
    return {"date": date, "title": title, "publisher": pub, "summary": ""}


def test_concerns_and_label_and_markdown():
    today = dt.date.today().isoformat()
    year = [_h("2026-03-01", "Nike shares slump as tariffs and weak China demand weigh"), _h("2026-02-01", "Nike cuts outlook, warns on tariffs"),
            _h("2026-01-15", "Nike stock jumps on strong quarter"), _h(today, "Nike downgraded at Broker as demand concerns mount"),
            _h(today, "Nike falls on weak sales"), _h(today, "Nike drops after guidance cut"), _h(today, "Nike slides on tariff fears"),
            _h("2026-01-02", "Adidas beats estimates")]
    drops = [_h("2026-04-01", "Nike forecasts surprise sales drop as China weakness hurts turnaround", "Reuters")]
    con = S.concerns(year, drops, ["NKE", "Nike"])
    keys = [t["key"] for t in con["themes"]]
    assert con["n"] == 8 and "tariffs" in keys and "china" in keys and "demand" in keys
    ex = [e for t in con["themes"] for e in t["examples"]]
    assert len({e["title"] for e in ex}) == len(ex)                      # a headline illustrates one theme only
    assert sum(e["publisher"] == "Reuters" and e["weight"] == 2 for e in ex) == 1   # the drop-day headline is shown, once
    assert con["tone"]["pos"] == 1 and con["tone"]["neg_30d"] == 4 and con["tone"]["pos_30d"] == 0
    profile = {"defaultKeyStatistics": {"sharesShort": 120, "sharesShortPriorMonth": 100, "shortRatio": 3.2, "shortPercentOfFloat": 0.12,
                                        "heldPercentInstitutions": 0.8, "heldPercentInsiders": 0.01, "dateShortInterest": 1758844800}}
    pos = S.positioning(profile, {"n": 30, "bullish": 4, "bearish": 10, "watchers": 50})
    assert abs(pos["short_change"] - 0.2) < 1e-9 and pos["short_date"] == "2025-09-26"
    an = {"bullish_now": 0.5, "bullish_3m": 0.6, "n_target_cuts": 3, "n_target_raises": 0}
    label, sig = S.sentiment_label(pos, an, {"y0_up_down_30d": (0, 4)}, con["tone"])
    codes = [c for c, _, _ in sig]
    assert label == "negative" and codes == ["analysts_less_bullish", "targets_cut", "revisions_down", "shorts_rising", "short_heavy",
                                             "crowd_bearish", "news_negative"]
    view = {"concerns": con, "positioning": pos, "label": label, "signals": sig}
    en = "\n".join(S.sentiment_markdown(view, "en"))
    he = "\n".join(S.sentiment_markdown(view, "he"))
    assert en.startswith("**Investor concerns and sentiment.**") and "**Sentiment: negative**" in en and "Short interest 12.0% of float (+20%" in en
    assert he.startswith("### חששות המשקיעים וסנטימנט") and "**סנטימנט: שלילי**" in he and "מכסים וסחר" in he and "StockTwits" in he
    for c in codes:
        assert S.SIGNAL_EN[c].format(**{k: "" for k in ("now", "ago", "cuts", "raises", "up", "down", "chg", "pct", "bull", "bear", "n", "neg", "pos")})
    # positive / mixed labels and the empty case
    label2, _ = S.sentiment_label({"twits": {}}, {"bullish_now": 0.7, "bullish_3m": 0.5, "n_target_raises": 2, "n_target_cuts": 0}, {}, {})
    assert label2 == "positive"
    empty = S.concerns([], [], ["X"])
    assert empty["themes"] == [] and "no negative headlines" in "\n".join(S.sentiment_markdown(
        {"concerns": empty, "positioning": {"twits": {}}, "label": "mixed", "signals": []}, "en"))
