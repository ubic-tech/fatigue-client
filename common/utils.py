import aiohttp
from config import *
from models.models import EndpointResponse


class StatusError(Exception):
    pass


async def request(url, *, method='post', expected_status=200, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, **kwargs) as resp:
            if resp.status != expected_status:
                raise StatusError(resp.status, await resp.text())
            return await resp.json()


async def get_endpoint_url_by_hash(hash_id, x_auth):
    resp = await request(UBIC_URL + V1_ENDPOINTS,
                         headers={"X-Authorization": x_auth},
                         json={"identifiers": [hash_id, ]})
    if resp is None:
        pass  # todo: validate
    return EndpointResponse(resp).endpoints[0].endpoint
