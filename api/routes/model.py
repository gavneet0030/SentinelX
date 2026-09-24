from fastapi import APIRouter


router = APIRouter(
    prefix="/model",
    tags=["model"],
)


@router.get("/info")
def model_info():

    return {
        "model": "SentinelX Risk Engine",
        "version": "0.1.0",
        "status": "development",
    }
