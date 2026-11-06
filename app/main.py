import os
from fastapi import FastAPI

app = FastAPI(title="Production Platform API")

SERVICE_NAME = os.getenv("SERVICE_NAME", "production-platform-api")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0-dev")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")


@app.get("/")
def get_root():
    return {
        "service": SERVICE_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
    }


@app.get("/health")
def get_health():
    return {"status": "ok"}
