import enum


class Sentiment(enum.Enum):
    """
    Enumerated sentiment categories for financial or market-related text.

    Values:
        BULLISH: Optimistic / positive outlook.
        BEARISH: Pessimistic / negative outlook.
        NEUTRAL: No clear positive or negative bias.
    """
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
