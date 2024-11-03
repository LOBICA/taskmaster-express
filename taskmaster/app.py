import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from . import __version__
from .ai import demo, messages, ws
from .auth.endpoints import router as auth_endpoints
from .endpoints import subscriptions, tasks, users
from .paypal import webhooks
from .settings import CORS_ORIGINS, FASTAPI_DOCUMENTATION

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if FASTAPI_DOCUMENTATION:
    docs_url = "/docs"
    redoc_url = "/redoc"
else:
    docs_url = None
    redoc_url = None

app = FastAPI(
    title="Taskmaster Express",
    version=__version__,
    docs_url=docs_url,
    redoc_url=redoc_url,
)

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
app.include_router(demo.router)
