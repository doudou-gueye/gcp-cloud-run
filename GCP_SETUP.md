# GCP Cloud Run Deployment Setup Guide

Complete guide to set up Workload Identity Federation for secure GitHub Actions to GCP authentication.

## 📋 Prerequisites

- ✅ GCP Project ID: `811599973236`
- ✅ GitHub Repository: `doudou-gueye/gcp-cloud-run`
- ✅ `gcloud` CLI installed locally ([Install Guide](https://cloud.google.com/sdk/docs/install))
- ✅ Owner/Admin access to both GCP project and GitHub repository

## 🔐 Step 1: Create a Service Account

Open your terminal and run:

```bash
# Set variables
export PROJECT_ID="811599973236"
export SERVICE_ACCOUNT_NAME="github-actions-runner"
export SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Create service account
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
  --display-name="GitHub Actions Runner for Cloud Run Deployments" \
  --project=${PROJECT_ID}

echo "✅ Service account created: ${SERVICE_ACCOUNT_EMAIL}"
```

## 🎯 Step 2: Grant IAM Roles

```bash
# Grant Cloud Run Admin role
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
  --role=roles/run.admin \
  --condition=None

# Grant Artifact Registry Writer role (to push Docker images)
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
  --role=roles/artifactregistry.writer \
  --condition=None

# Grant Service Account User role
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:${SERVICE_ACCOUNT_EMAIL} \
  --role=roles/iam.serviceAccountUser \
  --condition=None

echo "✅ IAM roles assigned"
```

## 🏊 Step 3: Create Workload Identity Pool

```bash
# Set pool name
export WORKLOAD_IDENTITY_POOL_ID="github-actions-pool"
export WORKLOAD_IDENTITY_POOL_DISPLAY_NAME="GitHub Actions Pool"

# Create the pool
gcloud iam workload-identity-pools create ${WORKLOAD_IDENTITY_POOL_ID} \
  --project=${PROJECT_ID} \
  --location=global \
  --display-name="${WORKLOAD_IDENTITY_POOL_DISPLAY_NAME}"

echo "✅ Workload Identity Pool created: ${WORKLOAD_IDENTITY_POOL_ID}"
```

## 🔌 Step 4: Create Workload Identity Provider

```bash
# Set provider name
export WORKLOAD_IDENTITY_PROVIDER_ID="github-provider"

# Create the OIDC provider
gcloud iam workload-identity-pools providers create-oidc ${WORKLOAD_IDENTITY_PROVIDER_ID} \
  --project=${PROJECT_ID} \
  --location=global \
  --workload-identity-pool=${WORKLOAD_IDENTITY_POOL_ID} \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.aud=assertion.aud,attribute.repository=assertion.repository" \
  --issuer-uri=https://token.actions.githubusercontent.com \
  --attribute-condition="assertion.repository_owner == 'doudou-gueye'"

echo "✅ Workload Identity Provider created"
```

## 🔐 Step 5: Configure Service Account Impersonation

```bash
# Set GitHub repository info
export GITHUB_REPO="doudou-gueye/gcp-cloud-run"

# Grant Workload Identity User role
gcloud iam service-accounts add-iam-policy-binding ${SERVICE_ACCOUNT_EMAIL} \
  --project=${PROJECT_ID} \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_ID}/locations/global/workloadIdentityPools/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${GITHUB_REPO}"

echo "✅ Service account impersonation configured"
```

## 📝 Step 6: Get Workload Identity Provider Resource Name

```bash
# Get the full resource name
export WIF_PROVIDER=$(gcloud iam workload-identity-pools providers describe ${WORKLOAD_IDENTITY_PROVIDER_ID} \
  --project=${PROJECT_ID} \
  --location=global \
  --workload-identity-pool=${WORKLOAD_IDENTITY_POOL_ID} \
  --format="value(name)")

echo "WIF Provider: ${WIF_PROVIDER}"
```

**Copy the output** - you'll need it in the next step.

Example output:
```
projects/811599973236/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider
```

## 🔑 Step 7: Add GitHub Repository Secrets

1. Go to your GitHub repository: https://github.com/doudou-gueye/gcp-cloud-run
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add the following:

### Secret 1: `WIF_PROVIDER`
- **Name:** `WIF_PROVIDER`
- **Value:** (Paste the output from Step 6)
  ```
  projects/811599973236/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider
  ```

### Secret 2: `WIF_SERVICE_ACCOUNT`
- **Name:** `WIF_SERVICE_ACCOUNT`
- **Value:**
  ```
  github-actions-runner@811599973236.iam.gserviceaccount.com
  ```

## 📦 Step 8: Create Artifact Registry Repository

Create a repository to store your Docker images:

```bash
# Create Artifact Registry repository
gcloud artifacts repositories create cloud-run-repo \
  --repository-format=docker \
  --location=us-central1 \
  --project=${PROJECT_ID} \
  --description="Repository for Cloud Run Docker images"

echo "✅ Artifact Registry repository created"
```

## 🚀 Step 9: Test the Deployment

Push a commit to the `main` branch to trigger the workflow:

```bash
# Add all files
git add .

# Commit
git commit -m "Initial Cloud Run deployment setup"

# Push to main
git push origin main
```

Monitor the deployment:
1. Go to your repository: https://github.com/doudou-gueye/gcp-cloud-run
2. Click on the **Actions** tab
3. Watch the workflow execute
4. Once complete, your service will be available at the Cloud Run URL

## ✅ Verify Deployment

After successful deployment, check your service:

```bash
# Get service URL
gcloud run services describe gcp-cloud-run-service \
  --region=us-central1 \
  --project=${PROJECT_ID} \
  --format='value(status.url)'

# Test the service
curl $(gcloud run services describe gcp-cloud-run-service \
  --region=us-central1 \
  --project=${PROJECT_ID} \
  --format='value(status.url)')
```

## 🔧 Workflow Configuration

The GitHub Actions workflow (`.github/workflows/deploy-cloud-run.yml`) includes:

- ✅ Workload Identity Federation authentication
- ✅ Docker image build
- ✅ Push to Artifact Registry
- ✅ Deploy to Cloud Run
- ✅ Service health check

**To customize:**

Edit `.github/workflows/deploy-cloud-run.yml` and change:

```yaml
SERVICE_NAME: "gcp-cloud-run-service"    # Your Cloud Run service name
REGION: "us-central1"                    # GCP region
ARTIFACT_REPO: "cloud-run-repo"          # Artifact Registry repo name
```

## 📊 Monitoring & Logs

View deployment logs:

```bash
# View Cloud Run logs
gcloud run services describe gcp-cloud-run-service \
  --region=us-central1 \
  --project=${PROJECT_ID}

# Stream logs in real-time
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=gcp-cloud-run-service" \
  --project=${PROJECT_ID} \
  --limit 50 \
  --format json
```

## 🐛 Troubleshooting

### Error: "Permission denied"
**Solution:** Verify all IAM roles are correctly assigned:
```bash
gcloud projects get-iam-policy ${PROJECT_ID} \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:${SERVICE_ACCOUNT_EMAIL}"
```

### Error: "Artifact Registry not found"
**Solution:** Create the repository (Step 8) or verify it exists:
```bash
gcloud artifacts repositories list --project=${PROJECT_ID}
```

### Error: "Cloud Run service not found"
**Solution:** The service will be created on first deployment. If it fails, check workflow logs in GitHub Actions.

### Error: "Image not found in Artifact Registry"
**Solution:** Verify Docker build succeeded in the workflow logs and that the service account has `artifactregistry.writer` role.

## 🔐 Security Best Practices

✅ **Workload Identity Federation** - No long-lived credentials stored
✅ **Service Account with Limited Permissions** - Only roles needed for Cloud Run and Artifact Registry
✅ **GitHub Secrets** - Securely stores WIF provider and service account email
✅ **OIDC Token** - Short-lived tokens exchanged for GCP credentials
✅ **Attribute Conditions** - Provider restricted to your GitHub organization

## 📚 Additional Resources

- [Google Cloud Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [GitHub Actions Google Cloud Auth](https://github.com/google-github-actions/auth)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Artifact Registry Documentation](https://cloud.google.com/artifact-registry/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📞 Need Help?

- Check GitHub Actions workflow logs for errors
- Review GCP Cloud Run logs for runtime issues
- Verify all IAM roles are correctly assigned
- Ensure Workload Identity Provider configuration matches your repository
