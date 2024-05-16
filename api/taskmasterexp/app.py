import logging
import sys

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from . import __version__
from .endpoints import tasks

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI(title="Taskmaster Express", version=__version__)


@app.get("/", response_class=PlainTextResponse)
async def root():
    return f"Taskmaster Express {__version__}"


@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"


app.include_router(tasks.router)
