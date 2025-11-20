# Thematic Trading Idea Agent

## Activate environment and install dependencies
```bash
source .venv/bin/activate
```

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## Run
```bash
.venv/bin/python src/main.py
```

## Debug Email MCP
`fastmcp` comes with built-in dashboard that allows you to mnually trigger tools as if you were an AI agent.

```bash
fastmcp dev src/mcp_server/email_server.py
```
* This will open a browser window with the MCP Inspector (`localhost:5173` or similar).
* Click on the `send_email` tool.
* Enter the recipient, subject and body of the email.
* Click on the `Run` button.
* The email will be sent to the recipient.

