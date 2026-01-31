import pytest
from api.endpoints import (
    create_booking, get_booking, get_bookings,
    create_token, update_booking, delete_booking
)
from utils.payloads import booking_payload, updated_booking_payload

@pytest.fixture(scope="module")
def token():
    return create_token("admin", "password123").json()["token"]

def test_booking_crud_flow(token):
    create = create_booking(booking_payload())
    booking_id = create.json()["bookingid"]

    get_resp = get_booking(booking_id)
    assert get_resp.status_code == 200

    update = update_booking(booking_id, updated_booking_payload(), token)
    assert update.status_code == 200

    delete = delete_booking(booking_id, token)
    assert delete.status_code in (200, 201)
