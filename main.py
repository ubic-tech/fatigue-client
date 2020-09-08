from fastapi import FastAPI
from core import OperationError
from starlette.responses import JSONResponse
from routers.drivers import router, PREFIX_URL
from config import AggregatorConfig

#  uvicorn main:app  --port 8080
app = FastAPI()


@app.exception_handler(OperationError)
async def attribute_exists(request, exc):
    return JSONResponse({"error": str(exc)}, status_code=503)


app.include_router(
    router,
    prefix=PREFIX_URL
)


@app.on_event("startup")
async def init_app():
    print(AggregatorConfig.AGGR_NAME, " started, hash id == ",
          AggregatorConfig.AGGR_HASH_ID)


@app.on_event("shutdown")
async def close_app():
    print(AggregatorConfig.AGGR_NAME, " finished, hash id == ",
          AggregatorConfig.AGGR_HASH_ID)
