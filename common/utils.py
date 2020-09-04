import aiohttp
from re import search, findall, sub
from config import AggregatorConfig
from models.models import EndpointResponse
from datetime import datetime, date, time


class StatusError(Exception):
    pass


async def request(url, *, method='post', expected_status=200, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, **kwargs) as resp:
            if resp.status != expected_status:
                raise StatusError(resp.status, await resp.text())
            return await resp.json()


async def get_endpoint_url_by_hash(hash_id) -> str:
    route = AggregatorConfig.UBIC_URL + AggregatorConfig.ENDPOINTS_ROUTE
    resp = await request(route, json={"identifiers": [hash_id, ]})
    if resp is None:
        pass  # todo: validate
    return EndpointResponse(**resp).endpoints[0].endpoint


def timestamp_to_datetime(timestamp: str) -> datetime:
    pattern = "{year}-{month}-{day}T{hour}:{minute}:{second}Z"

    # re stuff
    regex = sub(r'{(.+?)}', r'(?P<_\1>.+)', pattern)
    values = list(search(regex, timestamp).groups())
    keys = findall(r'{(.+?)}', pattern)

    #  values to int
    for i in range(len(values)):
        values[i] = int(values[i])

    _dict = dict(zip(keys, values))
    d = date(_dict["year"], _dict["month"], _dict["day"])
    t = time(_dict["hour"], _dict["minute"], _dict["second"])

    return datetime.combine(d, t)
