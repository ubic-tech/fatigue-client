from fastapi import FastAPI
from mpc import OperationError
from starlette.responses import JSONResponse
from router import router

#  uvicorn main:app  --port 8080
app = FastAPI()


@app.exception_handler(OperationError)
async def attribute_exists(request, exc):
    return JSONResponse({"error": str(exc)}, status_code=503)


app.include_router(
    router,
    prefix="/v1"
)


@app.on_event("startup")
async def init_app():
    pass


@app.on_event("shutdown")
async def close_app():
    pass
