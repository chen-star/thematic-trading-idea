FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# git is often needed for installing python packages from git repositories
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV PYTHONPATH=/app/src

# Command to run the application
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
