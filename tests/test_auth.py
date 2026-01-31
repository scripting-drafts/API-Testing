from api.endpoints import create_token

def test_create_token():
    resp = create_token("admin", "password123")
    assert resp.status_code == 200
    assert "token" in resp.json()
