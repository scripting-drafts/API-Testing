def booking_payload():
    return {
        "firstname": "Test",
        "lastname": "User",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-01-01",
            "checkout": "2026-01-05"
        },
        "additionalneeds": "Breakfast"
    }

def updated_booking_payload():
    return {
        "firstname": "Updated",
        "lastname": "User",
        "totalprice": 150,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-02-01",
            "checkout": "2026-02-05"
        },
        "additionalneeds": "Dinner"
    }
