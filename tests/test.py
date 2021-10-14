import requests
from bs4 import BeautifulSoup

r = requests.get("http://nginx")

r2 = requests.post("http://nginx",
                   data={
                       "email": "test@test.com",
                       "g-recaptcha-response": True
                   })

soup = BeautifulSoup(r2.content, "html.parser")

s = soup.find(id="key").contents
API_KEY = s[0]
api_url = f"http://nginx/FY/GOOG"
headers = {"Authorization": "Token " + API_KEY}

r3 = requests.get(api_url, headers=headers)

print(r3.content)
