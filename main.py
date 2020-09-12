from datetime import datetime
from random import seed

from fastapi import FastAPI
from utils.utils import OperationError
from starlette.responses import JSONResponse

from routers import drivers, health
from config import AggregatorConfig, PREFIX_URL


#  uvicorn main:app  --port 8080
app = FastAPI()


@app.exception_handler(OperationError)
async def attribute_exists(request, exc):
    return JSONResponse({"error": str(exc)}, status_code=503)


for r in (drivers.router, health.router):
    app.include_router(r, prefix=PREFIX_URL)


@app.on_event("startup")
async def init_app():
    seed(datetime.now().microsecond)
    print(AggregatorConfig.AGGR_NAME, " started, uuid == ",
          AggregatorConfig.AGGR_UUID)


@app.on_event("shutdown")
async def close_app():
    print(AggregatorConfig.AGGR_NAME, " finished, hash id == ",
          AggregatorConfig.AGGR_UUID)
