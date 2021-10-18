import requests
from django.conf import settings


def captcha_validate(captcha):
    """Check if the user is a human

    Args:
        captcha g-recaptcha-response object: response from google's
        captcha verification API

    Returns:
        Dict: A dictionary indicating whether captcha verification was 
        successful 
    """
    # hook for testing
    if settings.APPLICATION_UNDER_TEST:
        return {"success": True}

    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {"secret": settings.RECAPTCHA_PRIVATE_KEY, "response": captcha}
    response = requests.get(url, params=params, verify=True)
    return response.json()
