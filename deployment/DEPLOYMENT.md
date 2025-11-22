# How to Deploy to Google Cloud Platform (GCP)

This project is set up to be deployed as a **Cloud Run** service using a **Streamlit** web interface.

## Prerequisites

1.  **GCP Project**: You need a Google Cloud Project.
2.  **gcloud CLI**: Installed and authenticated (`gcloud auth login`).
3.  **Billing**: Enabled on your GCP project.

## Deployment Steps

### Using Cloud Build

This method builds the Docker image in the cloud and deploys it automatically.

0. **Set up GCP Project**
   ```bash
   gcloud config set project <your-project-id>
   ```

1.  **Enable Services**:
    ```bash
    gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com
    ```

2.  **Submit Build**:
    Run this command from the project root:
    ```bash
    gcloud builds submit --config deployment/cloudbuild.yaml .
    ```
    *Replace `us-central1` in `deployment/cloudbuild.yaml` if you prefer a different region.*

3.  **Access App**:
    Once the build and deployment finish, the terminal will show a **Service URL**. Click it to open your Trading Agent!

## Configuration

### Environment Variables
Your application requires several environment variables to function correctly. You must set these in your Cloud Run service.

**Required Variables:**
- `GOOGLE_API_KEY`: Your Google Gemini API Key.
- `FINNHUB_API_KEY`: API Key for Finnhub stock data.
- `BLUESKY_USERNAME`: Your Bluesky username.
- `BLUESKY_APP_PASSWORD`: Your Bluesky app password.
- `EMAIL_USER`: Email address for sending reports.
- `EMAIL_PASSWORD`: App password for the email account.
- `SMTP_SERVER`: (Optional) Defaults to `smtp.gmail.com`.
- `SMTP_PORT`: (Optional) Defaults to `587`.

**How to set them:**
1.  Go to the [Cloud Run Console](https://console.cloud.google.com/run).
2.  Click on your service (`trading-agent`).
3.  Click **Edit & Deploy New Revision**.
4.  Go to the **Variables & Secrets** tab.
5.  Add each variable under "Environment variables".
6.  Click **Deploy**.

Alternatively, you can set them via command line during deployment (not recommended for secrets) or update them:
```bash
gcloud run services update trading-agent --set-env-vars GOOGLE_API_KEY=value,FINNHUB_API_KEY=value
```

### Compute Resources
If your agent runs out of memory or is slow, you can increase resources:
- **Memory**: Default is usually 512MB. You might need 1GB or 2GB.
- **CPU**: Default is 1 vCPU.

To update:
```bash
gcloud run services update trading-agent --memory 2Gi --cpu 2
```

## Maintenance

### Updating the Application
To deploy a new version of your code:
1.  Make your code changes.
2.  Run the build command again:
    ```bash
    gcloud builds submit --config deployment/cloudbuild.yaml .
    ```
    This will build a new image and update the Cloud Run service automatically.

### Viewing Logs
To debug issues or see agent output:
1.  Go to the [Cloud Run Console](https://console.cloud.google.com/run).
2.  Click on your service.
3.  Click on the **Logs** tab.
    You can filter by "Error" or "Info" to see what's happening.

## Local Testing

To test the web interface locally before deploying:

1.  **Install Streamlit**:
    ```bash
    pip install streamlit watchdog
    ```

2.  **Run App**:
    ```bash
    export PYTHONPATH=$PYTHONPATH:$(pwd)/src
    streamlit run src/streamlit_app.py

## Troubleshooting

### 403 Forbidden Error
If you see a `403 Forbidden` error when accessing the URL, it means the service is not publicly accessible. Run this command to allow public access:

```bash
gcloud run services add-iam-policy-binding trading-agent \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --region=us-central1
```

### Restricting Access (Private Service)

If you want to make the service private (accessible only to you):

1.  **Remove Public Access**:
    ```bash
    gcloud run services remove-iam-policy-binding trading-agent \
        --member="allUsers" \
        --role="roles/run.invoker" \
        --region=us-central1
    ```

2.  **Grant Yourself Access**:
    (You likely already have access as the owner, but to be sure):
    ```bash
    gcloud run services add-iam-policy-binding trading-agent \
        --member="user:YOUR_EMAIL@gmail.com" \
        --role="roles/run.invoker" \
        --region=us-central1
    ```

3.  **Accessing a Private Service**:
    Since Cloud Run doesn't have a built-in login page, the easiest way to access a private service in your browser is using the Google Cloud proxy:
    ```bash
    gcloud run services proxy trading-agent --port=8080 --region=us-central1
    ```
    Then open `http://localhost:8080` in your browser. This creates a secure tunnel using your local credentials.

## Cleanup

To remove the deployed resources and avoid incurring charges:

1.  **Delete the Cloud Run Service**:
    ```bash
    gcloud run services delete trading-agent --region=us-central1
    ```

2.  **Delete the Container Image**:
    ```bash
    # List images to find the exact name if needed
    gcloud container images list-tags gcr.io/$PROJECT_ID/trading-agent

    # Delete the image (replace with your specific digest or tag if needed)
    gcloud container images delete gcr.io/$PROJECT_ID/trading-agent --force-delete-tags
    ```

3.  **Delete Cloud Build History** (Optional):
    You can view and delete build history in the [Cloud Build Console](https://console.cloud.google.com/cloud-build/builds).
