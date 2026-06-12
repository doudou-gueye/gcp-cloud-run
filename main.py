"""
Example FastAPI application for Google Cloud Run
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI(
    title="GCP Cloud Run Service",
    description="Example FastAPI application deployed to Google Cloud Run",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint - Health check"""
    return {
        "status": "healthy",
        "message": "Cloud Run service is running",
        "service": "gcp-cloud-run-service",
        "environment": os.getenv("ENV", "production")
    }


@app.get("/health")
async def health_check():
    """Kubernetes-style health check endpoint"""
    return {"status": "OK", "service": "ready"}


@app.get("/api/info")
async def service_info():
    """Get service information"""
    return {
        "name": "gcp-cloud-run-service",
        "version": "1.0.0",
        "environment": os.getenv("ENV", "production"),
        "region": os.getenv("REGION", "us-central1")
    }


@app.post("/api/echo")
async def echo(message: dict):
    """Echo endpoint - returns the received message"""
    return {
        "received": message,
        "status": "success"
    }


@app.get("/metrics")
async def metrics():
    """Metrics endpoint"""
    return {
        "uptime": "healthy",
        "requests_processed": 0,
        "errors": 0
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
