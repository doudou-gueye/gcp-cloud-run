# GCP Cloud Run Deployment

This repository contains a complete deployment pipeline for deploying FastAPI applications to Google Cloud Run using GitHub Actions with Workload Identity Federation for secure authentication.

## 🚀 Quick Start

1. **Follow the GCP setup guide** - See `GCP_SETUP.md` for complete Workload Identity Federation configuration
2. **Add GitHub secrets** - Configure `WIF_PROVIDER` and `WIF_SERVICE_ACCOUNT` in repository settings
3. **Deploy** - Push to `main` branch to trigger automatic deployment

## 📂 Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── deploy-cloud-run.yml    # GitHub Actions deployment workflow
├── Dockerfile                       # Container configuration
├── requirements.txt                 # Python dependencies
├── main.py                         # FastAPI application
├── GCP_SETUP.md                    # Setup instructions
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🔧 What's Included

### GitHub Actions Workflow
- Automated deployment on push to `main` branch
- Workload Identity Federation authentication (no stored credentials)
- Docker image build and push to Artifact Registry
- Cloud Run service deployment
- Service URL output

### FastAPI Application
- Health check endpoints (`/` and `/health`)
- Service info endpoint (`/api/info`)
- Echo endpoint (`/api/echo`)
- Metrics endpoint (`/metrics`)

### Configuration
- Python 3.11 slim Docker image
- FastAPI + Uvicorn
- Google Cloud Logging support
- 512MB memory, 1 CPU allocation
- Port 8080 configuration

## 📋 Prerequisites

- GCP Project with Cloud Run API enabled
- GitHub repository access
- `gcloud` CLI installed locally
- Workload Identity Federation configured (see GCP_SETUP.md)

## 🔐 Security Features

✅ **Workload Identity Federation** - No long-lived credentials
✅ **OIDC Token Exchange** - Short-lived tokens
✅ **Limited IAM Roles** - Minimal required permissions
✅ **GitHub Secrets** - Secure configuration storage
✅ **Attribute Conditions** - Repository-specific access control

## 📖 Documentation

- **GCP_SETUP.md** - Complete setup guide with step-by-step instructions
- **GitHub Actions** - Workflow configuration details in `.github/workflows/deploy-cloud-run.yml`
- **FastAPI** - Application code in `main.py`

## 🚀 Deployment Flow

1. Push code to `main` branch
2. GitHub Actions workflow triggers
3. Authenticates to GCP using Workload Identity Federation
4. Builds Docker image
5. Pushes to Artifact Registry
6. Deploys to Cloud Run
7. Returns service URL

## 📊 Monitoring

View your deployed service:
- Cloud Console: https://console.cloud.google.com/run
- Logs: `gcloud logging read ...`
- Service URL: Available in GitHub Actions workflow output

## 🔧 Customization

Edit `.github/workflows/deploy-cloud-run.yml` to change:
- Service name
- Region
- Memory/CPU allocation
- Environment variables

## 🐛 Troubleshooting

See **GCP_SETUP.md** troubleshooting section for common issues and solutions.

## 📚 Resources

- [Google Cloud Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

## 📝 License

This project is provided as-is for educational and deployment purposes.
