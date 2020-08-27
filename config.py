from common.config import env_config


@env_config
class AggregatorConfig:
    UBIC_URL: str = "http://127.0.0.1:8888"
    SHARES_ROUTE: str = "/v1/shares"
    ENDPOINTS_ROUTE: str = "/v1/endpoints"
    AGGR_HASH_ID: str = "fast"
