"""
Fetch Bluesky posts for a given stock ticker.

This module provides a small wrapper around the `atproto` SDK to search for
recent posts that include a cashtag (for example, `\$AAPL`). It expects Bluesky
credentials to be provided via environment variables and will authenticate the
client before issuing a search.

Requirements:
- atproto
- python-dotenv (optional, for loading a local .env file)

Environment variables:
- BLUESKY_USERNAME: Your Bluesky handle (for example, `user.bsky.social`)
- BLUESKY_APP_PASSWORD: An app password generated in Bluesky settings

Notes:
- On any authentication or network error, this module prints a short message
  and returns an empty list instead of raising.
- The search query uses a cashtag format (`\$TICKER`), which is commonly used
  in financial communities on Bluesky.
"""

# import os
from typing import List, Dict, Any

from atproto import Client
# from dotenv import load_dotenv

# load_dotenv()
#
# # --- Configuration ---
# # To get an App Password, go to Bluesky > Settings > Privacy & Security > App Passwords.
# BLUESKY_USERNAME: str | None = os.getenv("BLUESKY_USERNAME")
# BLUESKY_APP_PASSWORD: str | None = os.getenv("BLUESKY_APP_PASSWORD")


def get_bluesky_posts(symbol: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search for recent Bluesky posts containing a stock ticker cashtag and return
    normalized post data.

    Args:
        symbol: Stock ticker to search for (for example, `GOOG` or `AAPL`).
        limit: Maximum number of posts to request from the API.

    Returns:
        A list of dictionaries, one per post. Each dictionary contains:
        - `content` (str): Text content of the post.
        - `author` (str): Author handle (for example, `user.bsky.social`).
        - `like_count` (int | None): Number of likes if available.
        - `repost_count` (int | None): Number of reposts if available.
        - `created_at` (str): ISO 8601 timestamp when the post was created.
        - `uri` (str): The post URI.

        If credentials are missing or an error occurs during authentication or
        search, an empty list is returned and a short message is printed.

    Notes:
        - This function authenticates using the `BLUESKY_USERNAME` and
          `BLUESKY_APP_PASSWORD` environment variables.
        - The query uses the `\$SYMBOL` convention to match cashtags.
    """
    if not BLUESKY_USERNAME or not BLUESKY_APP_PASSWORD:
        print("🚨 Error: Please set your Bluesky username and app password.")
        return []

    # 1. Initialize and authenticate
    print(f"Connecting to Bluesky as {BLUESKY_USERNAME}...")
    try:
        client = Client()
        client.login(BLUESKY_USERNAME, BLUESKY_APP_PASSWORD)
    except Exception as e:
        print(f"Authentication failed: {e}")
        return []

    # 2. Define search query (cashtag format)
    search_query = f"${symbol.upper()}"
    print(f"Searching for posts containing: '{search_query}'")

    # 3. Perform the search
    try:
        response = client.app.bsky.feed.search_posts(
            params={
                "q": search_query,
                "sort": "latest",
                "lang": "en",
                "limit": limit,
            },
        )
    except Exception as e:
        print(f"Error during post search: {e}")
        return []

    # 4. Process and extract post data
    posts: List[Dict[str, Any]] = []
    for post_view in response.posts:
        # Skip posts without text
        if getattr(post_view.record, "text", None) is None:
            continue

        posts.append(
            {
                "content": post_view.record.text,
                "author": post_view.author.handle,
                "like_count": getattr(post_view, "like_count", None),
                "repost_count": getattr(post_view, "repost_count", None),
                "created_at": getattr(post_view.record, "created_at", ""),
                "uri": post_view.uri,
            }
        )

    return posts


# --- Execution ---
if __name__ == "__main__":
    # REPLACE 'GOOG' with the stock ticker you want to search
    STOCK_TICKER_SYMBOL = "GOOG"
    POST_LIMIT = 10

    relevant_posts = get_bluesky_posts(STOCK_TICKER_SYMBOL, POST_LIMIT)

    print(f"\n--- Found {len(relevant_posts)} BlueSky posts for ${STOCK_TICKER_SYMBOL} ---")

    for i, post in enumerate(relevant_posts):
        print(f"\n#{i + 1} by @{post['author']}")
        print(f"Posted: {post['created_at'].split('T')[0] if post['created_at'] else ''}")
        print(f"Likes: {post['like_count']}, Reposts: {post['repost_count']}")
        print(f"Content: {post['content']}")
        print("-" * 20)