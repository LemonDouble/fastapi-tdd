from fastapi import FastAPI, HTTPException
import logging.config

logging.config.fileConfig("logging.config", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def test():
    try:
        result = 1 / 0
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error occurred: {e}")