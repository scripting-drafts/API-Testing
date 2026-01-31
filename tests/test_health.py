from api.endpoints import ping

def test_api_health():
    resp = ping()
    assert resp.status_code in (200, 201)
