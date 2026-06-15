#!/usr/bin/env python3
import os, sys, json, urllib.request, glob

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

def process_markdown_posts(api_key):
    posted_urls = []
    # Find all markdown files in the 'posts' folder
    for md_path in sorted(glob.glob('posts/*.md')):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if not content:
            # Skip empty files
            continue
        # Post the raw markdown content as plain text (Binance Square only accepts plain text)
        result = post_to_square(content, api_key)
        if result.get('code') == '000000':
            post_id = result.get('data', {}).get('id')
            if post_id:
                url = f"https://www.binance.com/square/post/{post_id}"
                posted_urls.append((md_path, url))
                print(f"Posted {md_path} -> {url}")
            else:
                print(f"Posted {md_path} but no ID returned", file=sys.stderr)
        else:
            print(f"Failed to post {md_path}: {result}", file=sys.stderr)
        # Delete the markdown file after attempting to post (whether success or failure)
        try:
            os.remove(md_path)
            print(f"Deleted {md_path}")
        except OSError as e:
            print(f"Error deleting {md_path}: {e}", file=sys.stderr)
    return posted_urls

def main():
    api_key = os.getenv('BINANCE_SQUARE_API_KEY')
    if not api_key:
        print('Error: BINANCE_SQUARE_API_KEY not set', file=sys.stderr)
        sys.exit(1)
    # If there are any markdown posts, process them
    if os.path.isdir('posts'):
        posted = process_markdown_posts(api_key)
        if posted:
            # Build a simple notification message
            msg_lines = ['✅ Posted the following Binance Square items:']
            for path, url in posted:
                msg_lines.append(f'- {os.path.basename(path)}: {url}')
            # Output notification for GitHub Actions logs (could be captured by a notification step)
            print('\n'.join(msg_lines))
    else:
        print('No posts folder found; nothing to do.')

if __name__ == '__main__':
    main()
