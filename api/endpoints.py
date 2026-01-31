from api.client import APIClient

client = APIClient()

def ping():
    return client.request("GET", "/ping")

def create_token(username, password):
    return client.request("POST", "/auth", json={
        "username": username,
        "password": password
    })

def get_booking(booking_id):
    return client.request("GET", f"/booking/{booking_id}")

def get_bookings():
    return client.request("GET", "/booking")

def create_booking(payload):
    return client.request("POST", "/booking", json=payload,
                          headers={"Content-Type": "application/json"})

def update_booking(booking_id, payload, token):
    return client.request("PUT", f"/booking/{booking_id}", json=payload,
                          headers={
                              "Content-Type": "application/json",
                              "Cookie": f"token={token}"
                          })

def delete_booking(booking_id, token):
    return client.request("DELETE", f"/booking/{booking_id}",
                          headers={"Cookie": f"token={token}"})
