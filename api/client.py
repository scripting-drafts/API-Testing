import requests
from utils.config import BASE_URL

class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        return self.session.request(method, url, **kwargs)
