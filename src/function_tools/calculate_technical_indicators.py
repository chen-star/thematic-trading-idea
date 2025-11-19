import ta as ta_lib
import warnings

warnings.filterwarnings(
    action="ignore",
    message=".*invalid value encountered in.*",
    category=RuntimeWarning
)

def calculate_technical_indicators(df):
    """
    Compute SMA \(20\), RSI \(14\), and MACD histogram \(12, 26, 9\) for the given DataFrame.

    Parameters:
        df (pandas.DataFrame): Price history with at least a `Close` column
            convertible to `float`. Data should be in ascending chronological order.

    Returns:
        pandas.DataFrame: A copy of the input with additional columns:
            - `SMA_20` \(float\): 20-period simple moving average of `Close`.
            - `RSI_14` \(float\): 14-period relative strength index.
            - `MACDh_12_26_9` \(float\): MACD histogram \(MACD line - signal line\).

        If `df` is empty, the original `df` is returned unchanged.

    Notes:
        - Missing values are not filled; downstream consumers should handle `NaN`s.
        - The first non-`NaN` values appear only after sufficient lookback
          for each indicator.
    """
    if df.empty:
        return df

    df['Close'] = df['Close'].astype(float)
    df_filtered = df.copy()

    df_filtered['SMA_20'] = ta_lib.trend.sma_indicator(close=df_filtered['Close'], window=20, fillna=False)
    df_filtered['RSI_14'] = ta_lib.momentum.rsi(close=df_filtered['Close'], window=14, fillna=False)
    macd_instance = ta_lib.trend.MACD(close=df['Close'], window_fast=12, window_slow=26, window_sign=9, fillna=False)
    df_filtered['MACDh_12_26_9'] = macd_instance.macd_diff()

    return df_filtered


def generate_aggregated_signal(symbol, df):
    """
    Produce a majority-of-three sentiment signal from SMA, RSI, and MACD.

    Parameters:
        symbol (str): The asset ticker/symbol used for labeling the result.
        df (pandas.DataFrame): DataFrame that already contains indicator columns
            produced by `calculate_technical_indicators`. Rows with `NaN` in any
            required indicator are ignored for the decision.

    Returns:
        dict: A dictionary with:
            - `symbol` \(str\)
            - `aggregated_sentiment` \(str\): `BULLISH` \| `BEARISH` \| `NEUTRAL`
            - `justification` \(str\): Summary of votes and indicator statuses

        If there is not enough non-`NaN` data to evaluate, returns a `NEUTRAL`
        sentiment with a justification explaining the condition.
    """
    indicators_df = calculate_technical_indicators(df)

    valid_df = indicators_df.dropna()

    if valid_df.empty:
        return {
            'symbol': symbol,
            'aggregated_sentiment': "NEUTRAL",
            'justification': "Insufficient historical data (min ~26 days required)"
        }

    latest = valid_df.iloc[-1]

    bullish_count = 0
    bearish_count = 0
    indicator_status = {}

    # --- Indicator Status Check ---
    if latest['Close'] > latest['SMA_20']:
        bullish_count += 1
        indicator_status['SMA'] = "Bullish (Price > SMA)"
    elif latest['Close'] < latest['SMA_20']:
        bearish_count += 1
        indicator_status['SMA'] = "Bearish (Price < SMA)"
    else:
        indicator_status['SMA'] = "Neutral (Price = SMA)"

    if latest['RSI_14'] > 50:
        bullish_count += 1
        indicator_status['RSI'] = "Bullish (Momentum > 50)"
    elif latest['RSI_14'] < 50:
        bearish_count += 1
        indicator_status['RSI'] = "Bearish (Momentum < 50)"
    else:
        indicator_status['RSI'] = "Neutral (RSI = 50)"

    if latest['MACDh_12_26_9'] > 0:
        bullish_count += 1
        indicator_status['MACD'] = "Bullish (MACD Line > Signal Line)"
    elif latest['MACDh_12_26_9'] < 0:
        bearish_count += 1
        indicator_status['MACD'] = "Bearish (MACD Line < Signal Line)"
    else:
        indicator_status['MACD'] = "Neutral (MACD Crossover Point)"

    # --- Majority Decision & Final Justification String ---
    if bullish_count >= 2:
        final_signal = "BULLISH"
    elif bearish_count >= 2:
        final_signal = "BEARISH"
    else:
        final_signal = "NEUTRAL"

    justification = (
        f"Consensus: {bullish_count}/3 Bullish, {bearish_count}/3 Bearish. "
        f"SMA: {indicator_status['SMA']}; "
        f"RSI: {indicator_status['RSI']}; "
        f"MACD: {indicator_status['MACD']}"
    )

    return {
        'symbol': symbol,
        'aggregated_sentiment': final_signal,
        'justification': justification
    }