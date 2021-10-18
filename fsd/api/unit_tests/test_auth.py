from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AuthTest(TestCase):
    def setUp(self):
        user_email = "test@test.com"
        self.user = User.objects.create_user(username=user_email,
                                             email=user_email)
        Token.objects.create(user=self.user)

    def test_token_exists(self):
        token = Token.objects.get(user=self.user)
        self.assertIsNotNone(token)