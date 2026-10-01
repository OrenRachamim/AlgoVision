"""Build a tradable US stock universe and cache its price history.

1. Pull every listed stock from the Nasdaq screener (all US exchanges) with sector/industry.
2. Drop ETFs, test issues, preferreds, warrants, units, rights and notes.
3. Pre-filter on the latest price and volume, then download daily OHLCV history.
4. Final liquidity filter on history: median 60-day dollar volume, price, and length of history.

Usage: python universe.py [--years 3] [--min-dv 20e6] [--min-price 5] [--cache DIR]
Writes DIR/universe.csv, DIR/close.pkl, DIR/volume.pkl
"""
import argparse
import io
import pathlib
import time

import numpy as np
import pandas as pd
import requests
import yfinance as yf

SCREENER = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&download=true"
SYMDIR = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqtraded.txt"
EXCLUDE_NAME = r"(?i)\b(?:warrant|warrants|right|rights|unit|units|preferred|depositary shares? representing|notes? due|debentures?|% |trust preferred|acquisition corp)\b"
REFERENCE = ["SPY", "QQQ", "IWM", "RSP", "^VIX", "^TNX", "TLT", "UUP", "USO", "GLD", "HYG"]


def listed_stocks():
    hdr = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    rows = requests.get(SCREENER, headers=hdr, timeout=60).json()["data"]["rows"]
    df = pd.DataFrame(rows)
    sym = pd.read_csv(io.StringIO(requests.get(SYMDIR, timeout=60).text), sep="|")
    sym = sym[(sym["ETF"] == "N") & (sym["Test Issue"] == "N")]
    df = df[df.symbol.isin(set(sym.Symbol))]
    df = df[~df.symbol.str.contains(r"[\^/ ]")]
    df = df[~df.name.str.contains(EXCLUDE_NAME, regex=True)]
    df["price"] = pd.to_numeric(df.lastsale.str.replace(r"[$,]", "", regex=True), errors="coerce")
    df["mcap"] = pd.to_numeric(df.marketCap, errors="coerce")
    df["vol_today"] = pd.to_numeric(df.volume, errors="coerce")
    df["yf"] = df.symbol.str.replace(".", "-", regex=False)
    return df[["symbol", "yf", "name", "sector", "industry", "country", "ipoyear", "price", "mcap", "vol_today"]]


def download(tickers, years, batch=150):
    closes, vols = [], []
    for i in range(0, len(tickers), batch):
        chunk = tickers[i:i + batch]
        for attempt in range(4):
            try:
                d = yf.download(chunk, period=f"{years}y", auto_adjust=True, progress=False, threads=True)
                closes.append(d["Close"])
                vols.append(d["Volume"])
                break
            except Exception as e:  # rate limits: back off and retry
                print("retry", i, e)
                time.sleep(5 * 2 ** attempt)
        print(f"{min(i + batch, len(tickers))}/{len(tickers)}", flush=True)
    return pd.concat(closes, axis=1, sort=True), pd.concat(vols, axis=1, sort=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, default=3)
    ap.add_argument("--min-dv", type=float, default=20e6, help="median 60-day dollar volume")
    ap.add_argument("--min-price", type=float, default=5)
    ap.add_argument("--min-history", type=float, default=0.9, help="share of days with a price")
    ap.add_argument("--cache", default="cache")
    args = ap.parse_args()
    cache = pathlib.Path(args.cache)
    cache.mkdir(exist_ok=True)

    lst = listed_stocks()
    pre = lst[(lst.price >= args.min_price * 0.6) & (lst.price * lst.vol_today >= args.min_dv * 0.2)]
    print(f"listed {len(lst)}, pre-filter {len(pre)}")
    close, vol = download(sorted(set(pre.yf)) + REFERENCE, args.years)
    close = close.loc[:, ~close.columns.duplicated()]
    vol = vol.loc[:, ~vol.columns.duplicated()]

    dv = (close * vol).iloc[-60:].median()
    last = close.ffill().iloc[-1]
    hist = close.notna().mean()
    u = pre.set_index("yf")
    u["dv60"] = dv.reindex(u.index)
    u["last"] = last.reindex(u.index)
    u["history"] = hist.reindex(u.index)
    u["liquid"] = (u.dv60 >= args.min_dv) & (u["last"] >= args.min_price)
    u["full_history"] = u.history >= args.min_history
    u.to_csv(cache / "universe.csv")
    close.to_pickle(cache / "close.pkl")
    vol.to_pickle(cache / "volume.pkl")
    print(f"liquid {int(u.liquid.sum())}, liquid with full history {int((u.liquid & u.full_history).sum())}")


if __name__ == "__main__":
    main()
