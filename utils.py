from aio_requests import post
from config import *
from json import dumps
from models.models import EndpointResponse


async def get_endpoint_url_by_hash(hash_id, x_auth):
    headers = {
        "X-Authorization": x_auth
    }
    data = {
        "identifiers": [
            hash_id,
        ]
    }
    resp = await post(UBIC_URL + V1_ENDPOINTS, headers=headers, data=dumps(data))
    if resp is None:
        pass  # todo: validate
    return EndpointResponse(resp).endpoints[0].endpoint
