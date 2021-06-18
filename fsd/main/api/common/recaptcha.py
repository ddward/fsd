import requests
from django.conf import settings


def captcha_validate(captcha):
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {"secret": settings.RECAPTCHA_PRIVATE_KEY, "response": captcha}
    response = requests.get(url, params=params, verify=True)
    return response.json()
