from common.config import env_config


@env_config
class AggregatorConfig:
    UBIC_URL: str = "http://127.0.0.1:8888"
    SHARES_ROUTE: str = "/v1/shares"
    ENDPOINTS_ROUTE: str = "/v1/endpoints"
    AGGR_NAME: str = "Yandex"
    CLICK_HOUSE_URL: str = "archy1.dc"
