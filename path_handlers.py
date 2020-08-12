import json

ERROR = json.dumps({'code': "404", 'message': "NOT OK"})
SUCCESS = json.dumps({'code': "200", 'message': "OK"})


def _validate_put_request(handler):
    def wrapper(*args, **kwargs) -> str:
        headers = args[0]
        xauth = headers.get("X-Authorization", "")
        xreq = headers.get("X-Request-Id", "")
        if xauth == "" or xreq == "":
            return ERROR
        else:
            return handler(*args, **kwargs)
    return wrapper


def v1_health(_, __) -> str:
    """no params required. simply sends 'heartbeat'"""
    return SUCCESS


@_validate_put_request
def v1_drivers_fatigue(headers, body) -> str:
    """
    X-Authorization and X-Request-Id required
    stores data of tired drivers
    headers used in _validate_put_request
    """
    data = json.loads(body)
    try:
        drivers = data["drivers"]
    except KeyError:
        return ERROR
    print(drivers)
    return SUCCESS


def v1_drivers_online_hourly(headers, body) -> str:
    pass


def v1_drivers_online_quarter_hourly(headers, body) -> str:
    pass


def v1_drivers_on_order(headers, body) -> str:
    pass
