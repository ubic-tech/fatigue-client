from requests import post
from config import *
from json import dumps
from rest_models import EndpointResponse


def send(url, headers, data=""):
    return post(url, headers=headers, data=data).json()


def get_endpoint_url_by_hash(hash_id, x_auth):
    headers = {
        "X-Authorization": x_auth
    }
    data = {
        "identifiers": [
            hash_id,
        ]
    }
    r = send(UBIC_URL + V1_ENDPOINTS, headers=headers, data=dumps(data))  # todo: parse to Endpoints
    if r is None:
        pass  # todo: validate
    data = r.json()
    return EndpointResponse(data).endpoints[0].endpoint
