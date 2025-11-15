"""
HTTP retry policy for Google GenAI requests.

Notes:
- attempts: total tries including the initial attempt.
- exp_base: exponential backoff base; effective delay grows as initial_delay * (exp_base ** (n - 1)).
- initial_delay: seconds before the first retry.
- http_status_codes: only these transient HTTP errors will be retried.
"""

from google.genai import types

retry_config: types.HttpRetryOptions = types.HttpRetryOptions(
    attempts=5,  # Maximum total attempts (1 initial + 4 retries)
    exp_base=7,  # Exponential backoff base
    initial_delay=1,  # Start delay (seconds) before the first retry
    http_status_codes=[  # Retry on these HTTP status codes
        429,  # Too Many Requests (rate limit)
        500,  # Internal Server Error
        503,  # Service Unavailable
        504,  # Gateway Timeout
    ],
)
