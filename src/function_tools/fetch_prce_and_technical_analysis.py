from src.function_tools.calculate_technical_indicators import generate_aggregated_signal
from src.function_tools.fetch_yahoo_finance_stock_price import fetch_historical_close_prices


def fetch_price_and_technical_analysis(symbols: list) -> list:
    """
    Fetch historical price data and generate technical analysis signals for multiple symbols.
    Args:
        symbols (list of str): Stock ticker symbols to analyze (e.g., `["AAPL", "MSFT"]`).

    Returns:
        list of dict: A list where each dict corresponds to one symbol and contains:
            - `symbol` (str): The ticker symbol.
            - `aggregated_sentiment` (str): Overall sentiment (`BULLISH` | `BEARISH` | `NEUTRAL`).
            - `justification` (str): Human-readable explanation of the sentiment decision,
              including indicator votes (SMA, RSI, MACD).

        If a symbol does not have enough historical data to compute indicators, its entry will
        have a `NEUTRAL` sentiment with a justification explaining the condition.

    Example:
    [{'symbol': 'GOOG',
      'aggregated_sentiment': 'BEARISH',
      'justification': 'Consensus: 0/3 Bullish, 3/3 Bearish. SMA: Bearish (Price < SMA); RSI: Bearish (Momentum < 50); MACD: Bearish (MACD Line < Signal Line)'},
     {'symbol': 'TSLA',
      'aggregated_sentiment': 'BEARISH',
      'justification': 'Consensus: 0/3 Bullish, 3/3 Bearish. SMA: Bearish (Price < SMA); RSI: Bearish (Momentum < 50); MACD: Bearish (MACD Line < Signal Line)'},
     {'symbol': 'MSFT',
      'aggregated_sentiment': 'BEARISH',
      'justification': 'Consensus: 0/3 Bullish, 3/3 Bearish. SMA: Bearish (Price < SMA); RSI: Bearish (Momentum < 50); MACD: Bearish (MACD Line < Signal Line)'}]
    """
    structured_data_df = fetch_historical_close_prices(symbols)

    # Iterate through each symbol, perform analysis, and collect results
    final_analysis_list = []

    unique_symbols = structured_data_df['Symbol'].unique()
    print(f"\n--- Starting Technical Analysis for {len(unique_symbols)} Symbols ---")

    for symbol in unique_symbols:
        # Get data for the current symbol only
        symbol_df = structured_data_df[structured_data_df['Symbol'] == symbol].copy().reset_index(drop=True)

        # Generate the signal and justification based on the latest data point
        aggregated_json = generate_aggregated_signal(symbol, symbol_df)

        # Store the result
        final_analysis_list.append(aggregated_json)

    return final_analysis_list
