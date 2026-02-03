import os
import time
import random
from locust import HttpUser, task, between

USERNAME = os.getenv("RB_USERNAME", "admin")
PASSWORD = os.getenv("RB_PASSWORD", "password123")


class RestfulBookerUser(HttpUser):
    wait_time = between(0.2, 1.0)
    host = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
    token = None

    def on_start(self):
        self._authenticate_with_retry()
        if self.token:
            self.client.headers.update({"Cookie": f"token={self.token}"})

    def _authenticate_with_retry(self, max_attempts=5, wait_seconds=1.0):
        for _ in range(max_attempts):
            resp = self.client.post(
                "/auth",
                json={"username": USERNAME, "password": PASSWORD},
                name="POST /auth",
            )
            tok = None
            if resp.status_code == 200:
                try:
                    tok = resp.json().get("token")
                except Exception:
                    tok = None
            if tok:
                self.token = tok
                self.client.headers.update({"Cookie": f"token={self.token}"})
                return
            time.sleep(wait_seconds)

    @task(1)
    def ping(self):
        self.client.get("/ping", name="GET /ping")

    @task(1)
    def refresh_auth(self):
        self._authenticate_with_retry(max_attempts=1, wait_seconds=0.5)

    @task(2)
    def create_get_delete_booking(self):
        if not self.token:
            self._authenticate_with_retry()
            if not self.token:
                return

        payload = {
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": random.randint(50, 500),
            "depositpaid": True,
            "bookingdates": {"checkin": "2026-02-01", "checkout": "2026-02-03"},
            "additionalneeds": "Breakfast",
        }

        bid = None
        resp = self.client.post("/booking", json=payload, name="POST /booking")
        if resp.status_code in (200, 201):
            try:
                bid = resp.json().get("bookingid")
            except Exception:
                bid = None
        if not bid:
            return

        self.client.get(f"/booking/{bid}", name="GET /booking/{id}")

        def try_delete():
            del_resp = self.client.delete(f"/booking/{bid}", name="DELETE /booking/{id}")
            if del_resp.status_code in (200, 201, 204):
                return True
            if del_resp.status_code in (401, 403):
                return False
            return True

        ok = try_delete()
        if not ok:
            self._authenticate_with_retry(max_attempts=2, wait_seconds=0.5)
            if self.token:
                self.client.headers.update({"Cookie": f"token={self.token}"})
            try_delete()
