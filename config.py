from hashlib import sha256

from utils.config import env_config


def generate_id(x: str) -> str:
    return sha256(x.encode('utf-8')).hexdigest()


PREFIX_URL = "/v1"


@env_config
class AggregatorConfig:
    UBIC_URL: str = "http://127.0.0.1:8888"
    SHARES_ROUTE: str = "/v1/shares"
    ENDPOINTS_ROUTE: str = "/v1/endpoints"
    ENDPOINTS_TTL = 3600
    AGGR_NAME: str = "Yandex"
    AGGR_UUID: str = "8704d129-1af0-489e-b761-d40344c12e70"
    CLICK_HOUSE_URL: str = "archy1.dc"
