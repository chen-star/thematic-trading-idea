import datetime

import pandas as pd
import yfinance as yf


def fetch_historical_close_prices(symbols: list, days: int = 100) -> pd.DataFrame:
    """
    Fetches the last N days of daily closing prices for a list of stock symbols
    and formats the output into a single pandas DataFrame.

    Args:
        symbols (list): A list of stock ticker strings (e.g., ["GOOG", "TSLA"]).
        days (int): The number of days of historical data to retrieve.

    Returns:
        pd.DataFrame: A single DataFrame containing all fetched data,
                      with columns: ['Symbol', 'data' (Date), 'price' (Close Price)].
    """
    if not symbols:
        print("Error: The list of symbols is empty.")
        return pd.DataFrame()

    # Calculate the start date for the lookback period
    end_date = datetime.date.today()
    # Use 1.5x days to account for weekends/holidays and ensure 100 trading days are captured
    start_date = end_date - datetime.timedelta(days=days * 1.5)

    print(f"Fetching data for {symbols} from {start_date} to {end_date}...")

    # Use yfinance.download for bulk fetching, which is usually faster
    try:
        data = yf.download(
            tickers=symbols,
            start=start_date,
            end=end_date,
            interval="1d",
            progress=False  # Suppress download status messages
        )
    except Exception as e:
        print(f"An error occurred during data download: {e}")
        return pd.DataFrame()

    if data.empty:
        print("No data retrieved.")
        return pd.DataFrame()

    # Extract only the 'Close' column(s)
    close_data = data['Close']

    # Handle a single ticker case (yfinance returns a Series instead of a DataFrame with one column)
    if len(symbols) == 1:
        close_data = close_data.to_frame(name=symbols[0])

    # --- Collect all records into a single list ---
    all_records = []

    for symbol in symbols:
        if symbol in close_data.columns:
            # Drop NaN and get the last N days
            df_ticker = close_data[symbol].dropna().tail(days)

            # Convert the Series to the required list of dictionary format for the DataFrame
            for date, close_price in df_ticker.items():
                all_records.append({
                    "Symbol": symbol,
                    "Date": date.strftime('%Y-%m-%d'),
                    "Close": round(close_price, 4)
                })

            print(f"Successfully processed {symbol}: Retrieved {len(df_ticker)} records.")
        else:
            print(f"Warning: Could not find close price data for {symbol}.")

    # Convert the list of dictionaries into a single DataFrame
    final_df = pd.DataFrame(all_records)

    return final_df
