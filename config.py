from utils.config import env_config

PREFIX_URL = "/v1"


@env_config
class AggregatorConfig:
    UBIC_URL: str = "http://127.0.0.1:8888"
    SHARES_ROUTE: str = "/v1/shares"
    ENDPOINTS_ROUTE: str = "/v1/endpoints"
    ENDPOINTS_TTL = 3600
    AGGR_NAME: str = "Yandex"
    AGGR_UUID: str = "777aaaaa-1af0-489e-b761-d40344c12e70"
    CLICK_HOUSE_URL: str = "None"
