import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from . import __version__
from .auth.endpoints import router as auth_endpoints
from .endpoints import tasks

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI(title="Taskmaster Express", version=__version__)

origins = [
    "http://localhost:4200",
    "https://taskmaster.local"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=PlainTextResponse)
async def root():
    return f"Taskmaster Express {__version__}"


@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "pong"


app.include_router(auth_endpoints)
app.include_router(tasks.router)
