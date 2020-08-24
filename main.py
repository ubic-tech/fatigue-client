# Press Shift+F10 to execute it or replace it with your code.
from fastapi import FastAPI, Header, APIRouter
from config import *
from models.models import *
from aggregator import Aggregator
from logger.logger import log
from mpc import mpc_strategy, Violation
from starlette.responses import JSONResponse

#  uvicorn main:app  --port 8080


app = FastAPI()
router = APIRouter()
aggregator = Aggregator("Fast", 100500)  # use env vars (taxi-mpc)


def init():
    for driver in DRIVERS_DATA:
        name, license_id = driver
        aggregator.add_driver(name, license_id)
    log(aggregator.name, " inited")


@router.get("/health",
            response_model=ServerResponse,
            response_model_exclude_unset=True)
def v1_health():
    """simple heartbeat"""
    return SUCCESS


@router.post("/drivers/fatigue",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
def v1_drivers_fatigue(drivers_fatigue: DriversFatigue):
    """X-Authorization and X-Request-Id required
        stores data of tired drivers
        и что с этим делать?
        допустим пришло:
        {
            "timestamp": "2020-08-11T16:30:25.199",
            "drivers" : [
                {
                    "hash_id": "8xx8",
                    "online": "40",
                    "on_order": "20",
                },
                {
                    "hash_id": "8x7x8",
                    "online": "80",
                    "on_order": "20",
                },
            ]
        }
        какую реакцию запрогить?
        эмулировать блокировку как-то так: self.drivers[hash_id].block()?
        """
    print(drivers_fatigue)
    return SUCCESS


@router.post("/drivers/online/hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
def v1_drivers_online_hourly(request: OnlineHourly,
                             x_authorization: str = Header(...),
                             x_request_id: str = Header(...)):
    """как парсить json в кастомный объект?
    как забрать все хедеры разом в один (?)список?"""
    data_extractor = aggregator.drivers_db.get_online_hour
    route = "/v1/drivers/online/hourly"

    headers = {
        "X-Authorization": x_authorization,
        "X-Request-Id": x_request_id,
    }
    return mpc_strategy(headers, request, route, aggregator, data_extractor)


@router.post("/drivers/online/quarter_hourly",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
def v1_drivers_online_quarter_hourly(
        request: OnlineQuarterHourly):
    print(request)
    return SUCCESS  # exceptions


@router.post("/drivers/on_order",
             response_model=ServerResponse,
             response_model_exclude_unset=True)
def v1_drivers_on_order(request: OnOrder):
    print(request)
    return SUCCESS


@app.exception_handler(Violation)
async def attribute_exists(request, exc):
    return JSONResponse({"error": str(exc)}, status_code=503)


app.include_router(
    router,
    prefix="/v1"
)


init()
