from fastapi import FastAPI

from api.routes.transactions import router as transaction_router
from api.routes.risk import router as risk_router
from api.routes.alerts import router as alerts_router


def create_app() -> FastAPI:

    application = FastAPI(
        title="SentinelX",
        description=(
            "Real-Time Explainable Risk & "
            "Anomaly Intelligence Platform"
        ),
        version="0.1.0",
    )

    application.include_router(transaction_router)
    application.include_router(risk_router)
    application.include_router(alerts_router)

    @application.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "sentinelx-api",
        }

    return application


app = create_app()
