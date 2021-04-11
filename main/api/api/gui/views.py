from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from common.recaptcha import captcha_validate

# Create your views here.

HOME_PAGE = "gui/home_0.4.html"
COMPANY_PAGE = "gui/companies_table.html"


class LandingPage(View):
    def get(self, request):
        return render(request, HOME_PAGE)

    def post(self, request):
        form = self.request.POST
        email = form.get("email")
        captcha = form.get("g-recaptcha-response")
        if captcha:
            captcha_response = captcha_validate(captcha)
            if captcha_response["success"]:
                try:
                    user = User.objects.get(username=email)
                except User.DoesNotExist:
                    # password defaults to User.set_unusable_password()
                    # authentication handled by api token
                    user = User.objects.create_user(username=email, email=email)
                token, exists = Token.objects.get_or_create(user=user)
                return render(request, HOME_PAGE, {"token": token})

        return render(request, HOME_PAGE, {"captcha_warn": True})


class CompanyPage(View):
    def get(self, request):
        return render(request, COMPANY_PAGE)