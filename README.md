# Thematic Trading Idea Agent 🚀

An advanced AI-powered multi-agent system designed to discover, analyze, and report on thematic investment opportunities. By leveraging the power of Large Language Models (LLMs) and the Model Context Protocol (MCP), this tool automates the research process from idea generation to final report delivery.

> **What is Thematic Investing?**
>
> [Thematic investing](https://en.wikipedia.org/wiki/Thematic_investing) is an investment approach that focuses on predicted long-term trends rather than specific companies or sectors. It seeks to identify broad macro-level trends (e.g., disruptive technologies, climate change, changing demographics) and invest in companies poised to benefit from them.


## 🏗️ Architecture

![Architecture Diagram](architecture_diagram.png)

## 🌟 Overview

The **Thematic Trading Idea Agent** takes a user-defined investment theme (e.g., "AI Datacenters", "Green Hydrogen", "Cybersecurity") and deploys a team of specialized AI agents to:

1.  **Scan**: Identify relevant public companies associated with the theme.
2.  **Analyze**: A specialized team of analysts evaluates each ticker:
    *   **Technical Analysis**: Key indicators (SMA, RSI, MACD).
    *   **Institutional Ratings**: Institutional ratings.
    *   **Social Sentiment**: Trending discussions and sentiment from Bluesky.
3.  **Summarize**: Synthesize all data into a coherent investment thesis.
4.  **Deliver**: Email the final report directly to your inbox.

## ✨ Features

*   **Multi-Agent Architecture**: Orchestrates specialized agents (Scanner, Analyst, Summarizer, Emailer) for a comprehensive workflow.
*   **Real-Time Data**: Integrates with **Yahoo Finance** and **Finnhub** for up-to-date market data and ratings.
*   **Technical Analysis**: Automatically calculates key indicators like RSI, MACD, and Bollinger Bands.
*   **Social Intelligence**: Monitors **Bluesky** for trending discussions related to the tickers.
*   **MCP Integration**: Utilizes the **Model Context Protocol** (FastMCP) to securely handle email operations as a distinct service.
*   **Interactive CLI**: Features a polished, user-friendly command-line interface.

## 🛠️ Prerequisites

*   **Python 3.10+**
*   **pip** (or `uv` for faster dependency management)
*   **API Keys**:
    *   **Google Gemini**: For the LLM brains (`GOOGLE_API_KEY`).
    *   **Finnhub**: For stock data (`FINNHUB_API_KEY`).
    *   **Bluesky**: For social posts (`BLUESKY_USERNAME`, `BLUESKY_APP_PASSWORD`).
    *   **Gmail**: For sending reports (`EMAIL_USER`, `EMAIL_PASSWORD` - *App Password required*).

## 🚀 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/chen-star/thematic-trading-idea.git
    cd thematic-trading-idea
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv .venv
    # On Linux/MacOS:
    source .venv/bin/activate  
    # On Windows: 
    # .venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  **Set up Environment Variables**
    Copy the example configuration file:
    ```bash
    cp src/.env.example src/.env
    ```

2.  **Edit `src/.env`**
    Open `src/.env` in your editor and fill in the required values:

    ```ini
    # LLM Configuration
    GOOGLE_API_KEY=your_gemini_api_key
    GOOGLE_GENAI_USE_VERTEXAI=false

    # Social Media (Bluesky)
    BLUESKY_USERNAME=your_handle.bsky.social
    BLUESKY_APP_PASSWORD=your_app_password

    # Market Data
    FINNHUB_API_KEY=your_finnhub_key

    # Email Settings (Gmail Example)
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASSWORD=your_google_app_password
    ```

    > **Note**: For Gmail, you MUST use an **App Password** if 2FA is enabled. Go to [Google Account > Security > App Passwords](https://myaccount.google.com/apppasswords).

## 🏃 Usage

### Run the Agent
To start the interactive session:

```bash
.venv/bin/python src/main.py
```

1.  The CLI will launch with a welcome screen.
2.  Enter your desired **Thematic Topic** when prompted (e.g., *"Cloud Computing"*).
3.  Sit back as the agent team performs the analysis.
4.  Check your email for the final report!

### Debugging the Email Server (MCP)
The email functionality runs as a Model Context Protocol (MCP) server. You can test it in isolation using the MCP Inspector:

```bash
fastmcp dev src/mcp_server/email_server.py
```

*   This will open a web interface (usually at `localhost:5173`).
*   Select the `send_email` tool.
*   Fill in the arguments (to, subject, body) and click **Run** to test email delivery.

## 📂 Project Structure

```text
.
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── src/
    ├── agents/             # AI Agent definitions
    │   ├── analysts_team/  # Specialized analyst agents
    │   │   ├── institution_rating_analyst.py      # Analyzes institutional ratings
    │   │   ├── social_media_sentiment_analyst.py  # Analyzes social media sentiment
    │   │   └── technical_analyst.py               # Performs technical analysis
    │   ├── configs/        # Agent configurations
    │   │   ├── context_compaction_config.py       # Configuration for context compaction
    │   │   └── retry_config.py                    # Retry logic configuration
    │   ├── data_models/    # Pydantic models for agent data
    │   │   ├── institution_rating_agent_data_model.py
    │   │   ├── sentiment.py
    │   │   ├── social_media_sentiment_agent_data_model.py
    │   │   ├── technical_agent_data_model.py
    │   │   └── ticker_scanner_agent_data_model.py
    │   ├── plugin/         # Agent plugins
    │   │   └── count_model_call_plugin.py         # Plugin to count model calls
    │   ├── agent.py        # Base agent logic
    │   ├── email_agent.py  # Agent responsible for sending emails via MCP
    │   ├── summarize_agent.py      # Compiles the final report
    │   └── ticker_scanner_agent.py # Finds tickers for the theme
    ├── configs/            # Global application configurations
    │   └── settings.py     # Application settings
    ├── function_tools/     # Python tools used by agents
    │   ├── calculate_technical_indicators.py      # Calculates RSI, MACD, etc.
    │   ├── fetch_prce_and_technical_analysis.py   # Fetches price and runs analysis
    │   ├── fetch_yahoo_finance_stock_price.py     # Fetches stock data from Yahoo Finance
    │   ├── get_and_analyze_institution_rating.py  # Fetches institutional ratings
    │   └── get_bluesky_posts.py                   # Fetches posts from Bluesky
    ├── mcp_server/         # MCP Server implementations
    │   └── email_server.py # FastMCP server for email
    ├── utils/              # Helper utilities
    │   └── cli_utils.py    # CLI formatting and utilities
    └── main.py             # Application entry point
```


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
