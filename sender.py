from requests import post


def send(url, headers, data=""):
    return post(url, headers=headers, data=data).json()
