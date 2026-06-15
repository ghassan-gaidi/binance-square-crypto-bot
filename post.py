#!/usr/bin/env python3
import os, sys, json, urllib.request

def fetch_prices():
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum,binancecoin"
        "&vs_currencies=usd"
        "&include_24hr_change=true"
    )
    with urllib.request.urlopen(url, timeout=10) as resp:
        return json.load(resp)

def format_insight(prices):
    symbol_map = {"bitcoin": "BTC", "ethereum": "ETH", "binancecoin": "BNB"}
    lines = []
    for coin, data in prices.items():
        sym = symbol_map.get(coin, coin.upper())
        price = data.get("usd")
        change = data.get("usd_24h_change", 0.0)
        lines.append(f"{sym}: ${price:,.2f} ({change:+.2f}% 24h)")
    body = "Crypto Insight:\n" + "\n".join(lines) + "\n#Crypto #BinanceSquare"
    return body

def post_to_square(content, api_key):
    endpoint = "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add"
    payload = json.dumps({"bodyTextOnly": content}).encode()
    headers = {
        "X-Square-OpenAPI-Key": api_key,
        "Content-Type": "application/json",
        "clienttype": "binanceSkill",
    }
    req = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)

def main():
    api_key = os.getenv("BINANCE_SQUARE_API_KEY")
    if not api_key:
        print("Error: BINANCE_SQUARE_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    prices = fetch_prices()
    content = format_insight(prices)
    result = post_to_square(content, api_key)
    if result.get("code") == "000000":
        post_id = result.get("data", {}).get("id")
        if post_id:
            print(f"Successfully posted! URL: https://www.binance.com/square/post/{post_id}")
        else:
            print("Posted but no ID returned; check manually.", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Posting failed: {result}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
