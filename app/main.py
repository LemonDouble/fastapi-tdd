from fastapi import FastAPI
from app.routers import category_routes
import logging.config

logging.config.fileConfig("logging.config", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(category_routes.router, prefix="/api/category", tags=["Category"])