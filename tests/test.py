import unittest
import requests
from bs4 import BeautifulSoup


class TestFSD(unittest.TestCase):
    def test_site_up(self):
        r = requests.get("http://nginx")
        self.assertEqual(r.status_code, 200)

    def test_get_key(self):
        r = requests.post("http://nginx",
                          data={
                              "email": "test@test.com",
                              "g-recaptcha-response": True
                          })

        soup = BeautifulSoup(r.content, "html.parser")
        s = soup.find(id="key").contents
        API_KEY = s[0]
        self.assertEqual(len(API_KEY), 40)

    def test_api_call(self):
        r = requests.post("http://nginx",
                          data={
                              "email": "test@test.com",
                              "g-recaptcha-response": True
                          })

        soup = BeautifulSoup(r.content, "html.parser")
        s = soup.find(id="key").contents
        API_KEY = s[0]

        api_url = f"http://nginx/FY/GOOG"
        headers = {"Authorization": "Token " + API_KEY}

        r2 = requests.get(api_url, headers=headers)

        self.assertEqual(r2.json()[0]["ticker"], "GOOG")


if __name__ == '__main__':
    unittest.main()