"""Chart links for report tables (TradingView)."""

from __future__ import annotations

TRADINGVIEW = "https://www.tradingview.com/chart/?symbol={symbol}"


def tradingview_url(symbol: str) -> str:
    """Chart URL for a US ticker; TradingView resolves the primary listing itself (BRK.B, BF.B work as is)."""
    return TRADINGVIEW.format(symbol=str(symbol).strip().upper())


def tv(symbol: str) -> str:
    """Markdown link ``[SYM](url)`` used in every report table that lists tickers."""
    s = str(symbol).strip().upper()
    return f"[{s}]({tradingview_url(s)})"
