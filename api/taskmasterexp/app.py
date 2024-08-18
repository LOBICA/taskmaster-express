import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from . import __version__
from .auth.endpoints import router as auth_endpoints
from .chatbot import messages, ws
from .endpoints import subscriptions, tasks, users
from .paypal import webhooks
from .settings import CORS_ORIGINS

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI(title="Taskmaster Express", version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
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
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(subscriptions.router)
app.include_router(ws.router)
app.include_router(messages.router)
app.include_router(webhooks.router)
