"""
This script fetches the latest analyst stock recommendation trends from the Finnhub API
for a list of specified tickers. It processes the raw recommendation counts (Strong Buy, Buy,
Hold, Sell, Strong Sell) and aggregates them into a simple, three-category sentiment:
'bullish', 'bearish', or 'neutral'.

The Finnhub API key is loaded from an environment variable named 'FINNHUB_API_KEY'
using the python-dotenv library.
"""
import json
import os
import sys
from typing import Dict, Any, List

import finnhub
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# API_KEY is loaded from the environment variable FINNHUB_API_KEY
API_KEY: str | None = os.getenv("FINNHUB_API_KEY")


def analyze_recommendation_sentiment(finnhub_client: finnhub.Client, ticker: str) -> Dict[str, Any]:
    """
    Fetches the latest Analyst Recommendation Trends and calculates the aggregated
    sentiment (bullish, bearish, neutral) based on a custom logic.

    :param finnhub_client: An initialized Finnhub client instance.
    :type finnhub_client: finnhub.Client
    :param ticker: The stock ticker symbol (e.g., 'GOOG', 'TSLA').
    :type ticker: str
    :raises finnhub.exceptions.FinnhubAPIException: If the Finnhub API returns an error.
    :raises Exception: For any other unexpected error during processing.
    :returns: A dictionary containing the symbol, aggregated sentiment, and a detailed
              justification for the sentiment calculation.
    :rtype: Dict[str, Any]
    """
    try:
        # 1. Call the recommendation_trends endpoint
        data = finnhub_client.recommendation_trends(symbol=ticker)

        if not data:
            return {
                "symbol": ticker,
                "aggregated_sentiment": "N/A",
                "justification": "No recommendation data found for this ticker."
            }

        # 2. Use the latest (most recent) trend data object (data[0])
        latest_data = data[0]

        strong_buy = latest_data.get('strongBuy', 0)
        buy = latest_data.get('buy', 0)
        sell = latest_data.get('sell', 0)
        strong_sell = latest_data.get('strongSell', 0)
        hold = latest_data.get('hold', 0)  # Used for justification detail

        # 3. Apply the categorization decision logic
        total_buy = strong_buy + buy
        total_sell = sell + strong_sell

        if total_buy > total_sell:
            sentiment = "bullish"
        elif total_buy < total_sell:
            sentiment = "bearish"
        else:
            sentiment = "neutral"

        # 4. Construct the justification string
        justification = (
            f"Sentiment calculated as '{sentiment}' because Total Buy ({total_buy}) "
            f"was compared to Total Sell ({total_sell}). "
            f"Breakdown: Strong Buy={strong_buy}, Buy={buy}, Hold={hold}, Sell={sell}, Strong Sell={strong_sell}."
        )

        # 5. Return the required structured result object
        return {
            "symbol": ticker,
            "aggregated_sentiment": sentiment,
            "justification": justification
        }

    except finnhub.exceptions.FinnhubAPIException as api_err:
        return {
            "symbol": ticker,
            "aggregated_sentiment": "neutral",
            "justification": f"Finnhub API Error: {api_err}. Check API key and rate limits."
        }
    except Exception as e:
        return {
            "symbol": ticker,
            "aggregated_sentiment": "neutral",
            "justification": f"An unexpected error occurred: {e}"
        }


def run_analysis_for_multiple_tickers(tickers: List[str]) -> List[Dict[str, Any]]:
    """
    Initializes the Finnhub client and runs the sentiment analysis for all provided tickers.

    :param tickers: A list of stock ticker symbols to analyze.
    :type tickers: List[str]
    :returns: A list of dictionaries, where each dictionary contains the analysis
              result for a single ticker. Returns an empty list on configuration error.
    :rtype: List[Dict[str, Any]]
    """
    if not API_KEY or API_KEY == "YOUR_FINNHUB_API_KEY":
        print("Error: API_KEY is not set or is the placeholder.", file=sys.stderr)
        return []

    try:
        # Initialize the Finnhub Client
        finnhub_client = finnhub.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Error initializing Finnhub client: {e}", file=sys.stderr)
        return []

    results = []
    for ticker in tickers:
        # Log status to standard error to keep standard output clean for JSON
        print(f"Processing {ticker}...", file=sys.stderr)
        result = analyze_recommendation_sentiment(finnhub_client, ticker)
        results.append(result)

    return results


if __name__ == "__main__":
    # Example usage: Run analysis for a predefined list of symbols
    TICKERS_TO_ANALYZE = ["GOOG", "HIMS", "TSLA"]
    analysis_results = run_analysis_for_multiple_tickers(TICKERS_TO_ANALYZE)

    # Output the final list of analysis results as pretty-printed JSON
    print(json.dumps(analysis_results, indent=4))