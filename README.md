# Binance Square Crypto Bot

This repository contains a small Python script that automatically posts a short crypto insight to **Binance Square** on a configurable schedule using GitHub Actions.

## How it works
1. The workflow runs on the schedule you define (default: daily at 09:00 UTC).
2. It fetches the latest price and 24‑hour change for BTC, ETH and BNB from the public CoinGecko API.
3. It formats a concise text‑only message.
4. It posts the message to Binance Square via the OpenAPI endpoint using the secret `BINANCE_SQUARE_API_KEY`.
5. On success the script prints the post URL; on failure the workflow fails.

## Configuration
- **BINANCE_SQUARE_API_KEY** – Add this as a repository secret (the key you provided).
- **Schedule** – Edit `.github/workflows/post.yml` to change the cron expression.

## License
MIT – feel free to fork and adapt.
