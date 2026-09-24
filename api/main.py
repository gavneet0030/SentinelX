from fastapi import FastAPI

from api.routes.health import router as health_router
from api.routes.transactions import router as transaction_router
from api.routes.risk import router as risk_router
from api.routes.alerts import router as alerts_router
from api.routes.model import router as model_router


app = FastAPI(
    title="SentinelX",
    description="Real-Time Explainable Risk & Anomaly Intelligence Platform",
    version="0.1.0",
)


app.include_router(health_router)
app.include_router(transaction_router)
app.include_router(risk_router)
app.include_router(alerts_router)
app.include_router(model_router)


@app.get("/")
def root():
    return {
        "service": "SentinelX",
        "version": "0.1.0",
        "status": "operational",
    }
