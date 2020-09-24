import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
# from workers import rabbitmq
from magnet.config import rabbitmq
import magnet.user.views
import magnet.ingester.views
import magnet.research.views
import magnet.executor.views
import magnet.crawler.views
import magnet.trade.views
import magnet.develop.views

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    # return {"message": "Hello World"}
    return """
    <html>
    <head>
        <title>hello my application.</title>
    </head>
    <body>
        <a href="docs">docs</a><br>
        <a href="redoc">redoc</a><br>
    </body>
    </html>
    """

app.include_router(magnet.user.views.router, prefix="/users")
app.include_router(magnet.research.views.router, prefix="/research")
app.include_router(magnet.crawler.views.router, prefix="/crawler")
app.include_router(magnet.executor.views.router, prefix="/executor")
app.include_router(magnet.ingester.views.router, prefix="/ingester")
app.include_router(magnet.trade.views.router, prefix="/trade")
app.include_router(magnet.develop.views.router, prefix="/develop")


@app.on_event("startup")
async def startup_event():
    logger.info("startup fastapi app.")



@app.on_event("shutdown")
def shutdown_event():
    logger.info("shutdown fastapi app.")



