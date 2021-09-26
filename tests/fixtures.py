DATE_JSON = {
    "monday": [],
    "tuesday": [
        {
            "type": "open",
            "value": 36000
        },
        {
            "type" : "close",
            "value": 64800
        }
    ],
    "wednesday": [],
    "thursday": [
        {
            "type": "open",
            "value": 37800
        },
        {
            "type": "close",
            "value": 64800
        }
    ],
    "friday": [
        {
            "type": "open",
            "value": 36000
        }
    ],
    "saturday": [
        {
            "type": "close",
            "value": 3600
        },
        {
            "type": "open",
            "value": 36000
        }
    ],
    "sunday": [
        {
            "type": "close",
            "value": 3600
        },
        {
            "type": "open",
            "value": 43200
        },
        {
            "type": "close",
            "value": 75600
        }
    ]
}

DATE_RESULT = [
    "Monday: Closed",
    "Tuesday: 10 AM - 6 PM",
    "Wednesday: Closed",
    "Thursday: 10:30 AM - 6 PM",
    "Friday: 10 AM - 1 AM",
    "Saturday: 10 AM - 1 AM",
    "Sunday: 12 PM - 9 PM"
]

INVALID_JSON = {
    "monday": [],
    "tuesday": [
        {
            "key": "open",
            "value": 36000
        },
        {
            "key" : "close",
            "value": 64800
        }
    ]
}

MISSING_TYPES_JSON = {
    "monday": [],
    "tuesday": [
        {
            "type": "close",
            "value": 36000
        },
        {
            "type" : "close",
            "value": 64800
        }
    ],
    "wednesday": [],
    "thursday": [
        {
            "type": "open",
            "value": 37800
        },
        {
            "type": "open",
            "value": 64800
        }
    ]
}