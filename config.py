from utils.config import env_config
from hashlib import sha256


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
    AGGR_HASH_ID: str = generate_id(AGGR_NAME)
    CLICK_HOUSE_URL: str = "archy1.dc"
