from datetime import datetime

import aiohttp


class OperationError(Exception):
    pass


class StatusError(Exception):
    pass


async def request(url, *, method='post', expected_status=200, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.request(url=url, method=method, **kwargs) as resp:
            if resp.status != expected_status:
                raise StatusError(resp.status, await resp.text())
            return await resp.json()


def timestamp_to_datetime(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
