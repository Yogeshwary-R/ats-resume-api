from fastapi import FastAPI, Request
from fastapi.security import HTTPBearer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config import settings
from app.core.database import Base, engine
from app.routes.resume import router as resume_router
from app.routes.auth import router as auth_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.APP_NAME,
    description="Upload a resume and job description to get ATS score, matched skills, missing skills and AI suggestions.",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True}
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

security = HTTPBearer()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(resume_router, prefix="/resume", tags=["Resume"])

@app.get("/health")
@limiter.limit("10/minute")
def health_check(request: Request):
    logger.info("Health check called")
    return {
        "status": "running",
        "app": settings.APP_NAME
    }