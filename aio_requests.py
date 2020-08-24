import aiohttp


class StatusError(Exception):
    def __init__(self, status, text):
        self.status = status
        self.text = text


async def request(url, *, method='get', expected_status=200, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with getattr(session, method)(url, **kwargs) as resp:
            if resp.status != expected_status:
                raise StatusError(resp.status, await resp.text())
            return await resp.json()


async def get(url, expected_status=200, **kwargs):
    return await request(url, method='get', expected_status=expected_status, **kwargs)


async def post(url, expected_status=200, **kwargs):
    return await request(url, method='post', expected_status=expected_status, **kwargs)


async def put(url, expected_status=200, **kwargs):
    return await request(url, method='put', expected_status=expected_status, **kwargs)


async def patch(url, expected_status=200, **kwargs):
    return await request(url, method='patch', expected_status=expected_status, **kwargs)


async def delete(url, expected_status=200, **kwargs):
    return await request(url, method='delete', expected_status=expected_status, **kwargs)
