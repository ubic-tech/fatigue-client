headers = {
    "X-Authorization": "xauth",
    "X-Request-Id": "xreq",
}

drivers_fatigue_data = {
    "timestamp": "2020-08-11T16:30:25.199Z",
    "drivers": [
        {
            "hash_id": "Rogue101",
            "online": 100,
            "on_order": 50,
        },
        {
            "hash_id": "Harsh303",
            "online": 100,
            "on_order": 50,
        },
    ]
}

drivers_online_hourly_request_data = {
    "timestamp": "2020-08-11T16:30:25.199Z",
    "drivers": [
        {
            "hash_id": "Rogue101",
            "shares": [
                0
            ]
        },
        {
            "hash_id": "Harsh303",
            "shares": [
                1
            ]
        },
    ],
    "chain": [
        "9600",
    ],
}

drivers_online_quarter_hourly_request_data = {
    "timestamp": "2020-08-11T16:30:25.199Z",
    "drivers": [
        {
            "hash_id": "Tough202",
            "shares": [
                0, 1, 1, 0
            ]
        },
        {
            "hash_id": "Rigid505",
            "shares": [
                0, 0, 1, 1
            ]
        },
    ],
    "chain": [
        "9600",
    ],
}

drivers_on_order_data = {
    "timestamp": "2020-08-11T16:30:25.199Z",
    "drivers": [
        {
            "hash_id": "Tough202",
            "shares": [
                0
            ]
        },
        {
            "hash_id": "Rough505",
            "shares": [
                1
            ]
        },
    ],
    "chain": [
        "9600",
    ],
}
