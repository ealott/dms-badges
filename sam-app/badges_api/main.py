import logging
from badges_api.core.settings import settings
from badges_api.api.api_v1.api import api_router

from fastapi import FastAPI, Request, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from mangum import Mangum


#handler = Mangum(app, enable_lifespan = False)    

# def handler(event, context):
    # event['requestContext'] = {}  # Adds a dummy field; mangum will process this fine
    # 
    # app = FastAPI()
    # app.include_router(api_router, prefix=settings.API_V1_STR)
# 
    # @app.get('/')
    # async def homepage(
        # request: Request
        # ):
        # return HTMLResponse('<h1>Hello World</h1>')
# 
    # asgi_handler = Mangum(app)
    # response = asgi_handler(event, context)
# 
    # return response

from fastapi import FastAPI

from badges_api.api.api_v1.api import router as api_router
from mangum import Mangum

app = FastAPI()


@app.get("/")
async def root():
    return {"message`": "Hello World!"}


app.include_router(api_router, prefix="/api/v1")
handler = Mangum(app)