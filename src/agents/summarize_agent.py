from agents.configs.retry_config import retry_config
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

model = Gemini(
    model="gemini-2.5-flash-lite",
    retry_options=retry_config
)

# 2.  **Technical Analysis:** {structured_technical_analyst_findings}

PROMPT = """
# ROLE
Act as a Senior Equity Research Analyst writing a daily briefing. Your tone should be professional, objective, and concise.

# INPUT DATA
You will receive three sets of analysis findings in JSON/structured format:
1.  **Social Sentiment:** {structured_social_media_sentiment_findings}
2.  **Institutional Ratings:** {structured_institution_rating_findings}

# TASK
Synthesize these findings into a cohesive email summary. Do not just list the data; connect the dots. For example, if technicals are bullish but sentiment is negative, highlight this divergence as a risk factor.

# EMAIL STRUCTURE (HTML OUTPUT)
Generate the output as a single HTML block suitable for pasting directly into an email client (like Gmail). Follow these strict formatting rules:
-   **Format:** Use standard HTML `<table>`, `<tr>`, `<td>` tags for layout.
-   **Styling:** Use only **inline CSS** (e.g., `style="color: #2E7D32;"`). Do not use `<style>` blocks or external classes, as Gmail often strips them.
-   **Width:** Keep the content max-width to 600px for mobile readability.

## Content Sections:
1.  **Executive Summary (2-3 sentences):** A high-level verdict. Start with a clear signal (e.g., **STRONG BUY**, **NEUTRAL**, **SELL**).
2.  **Key Drivers:** A bulleted list of the 3 most critical factors driving this stock right now (mixing technical, social, and institutional data).
3.  **Deep Dive Table:** A summary table comparing the signals.

# TABLE FORMATTING INSTRUCTIONS
Create a table with headers: **Analysis Source**, **Signal (Bullish/Bearish/Neutral)**, and **Key Justification**.
-   Use a light grey background (`#f3f4f6`) for the header row.
-   **Color Coding:** Text for "Bullish" signals should be **Green** (`#137333`), "Bearish" should be **Red** (`#c5221f`), and "Neutral" should be **Grey** (`#5f6368`).
-   Ensure the table has a border (`border="1" style="border-collapse: collapse; width: 100%; border-color: #e0e0e0;"`).

# OUTPUT GENERATION
Produce *only* the HTML code for the email body.
"""

summarizer_agent = Agent(
    name="SummarizerAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=PROMPT,
    output_key="final_summary",
)

print("✅ summarizer_agent created.")
