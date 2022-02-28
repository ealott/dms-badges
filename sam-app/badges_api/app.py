import json
import logging

from fastapi import FastAPI, Request, Depends
from badges_api.core.settings import settings
from badges_api.api.api_v1.api import api_router
from starlette.requests import Request
from starlette.responses import HTMLResponse
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

# import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get('/hello')
async def homepage(
    request: Request
    ):
    return HTMLResponse('<h1>Hello World</h1>')

app.add_middleware(
    CORSMiddleware,
    allow_origins='http://evanlott.com, http://dallasmakerspace.org',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)