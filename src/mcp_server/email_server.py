import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()
email_recipient = os.getenv("EMAIL_USER")

# Initialize the MCP Server
mcp = FastMCP("email-service")


@mcp.tool()
def send_email(subject: str, html_body: str, recipient: str = email_recipient) -> str:
    """
    Sends an HTML email using SMTP.

    Args:
        subject: The subject line of the email.
        html_body: The content of the email (HTML format supported).
        recipient: The email address of the receiver.
    """
    # 1. specific configuration (Use Env Variables for security)
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        return "Error: EMAIL_USER or EMAIL_PASSWORD environment variables are not set."

    try:
        # 2. Create the email object
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient
        msg["Subject"] = subject

        # Attach the HTML body
        # We use 'html' as the second argument to render tables/bolding correctly
        msg.attach(MIMEText(html_body, "html"))

        # 3. Connect to the SMTP Server
        print(f"Connecting to {smtp_server}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection

        # 4. Login and Send
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()

        return f"Successfully sent email to {recipient}"

    except Exception as e:
        return f"Failed to send email. Error: {str(e)}"


if __name__ == "__main__":
    mcp.run()
