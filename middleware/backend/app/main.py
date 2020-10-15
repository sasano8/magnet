from fastapi.responses import HTMLResponse
from magnet import logger, rabbitmq, app
import magnet.user.views
import magnet.ingester.views
import magnet.research.views
import magnet.executor.views
import magnet.crawler.views
import magnet.trade.views
import magnet.trade_profile.views
import magnet.develop.views


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

# app.include_router(magnet.user.views.router, prefix="/users")
app.include_router(magnet.user.views.cbvrouter, prefix="/users")
app.include_router(magnet.research.views.router, prefix="/research")
app.include_router(magnet.crawler.views.router, prefix="/crawler")
app.include_router(magnet.executor.views.router, prefix="/executor")
app.include_router(magnet.ingester.views.router, prefix="/ingester")
app.include_router(magnet.trade.views.router, prefix="/trade")
app.include_router(magnet.trade_profile.views.router, prefix="/trade_profile")
app.include_router(magnet.develop.views.router, prefix="/develop")


@app.on_event("startup")
async def startup_event():
    logger.info("startup fastapi app!!!!!!!!")



@app.on_event("shutdown")
def shutdown_event():
    logger.info("shutdown fastapi app!!!!!!!")

