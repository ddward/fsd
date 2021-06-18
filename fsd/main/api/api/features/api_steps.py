import json

from aloe import before, step, world
from aloe.tools import guess_types

from django.contrib.auth.models import User

from rest_framework.test import APIClient, force_authenticate

from .. models import AnnualFullFormatted

@before.each_feature
def before_each_feature(feature):
    world.client = APIClient()

@step('the following rows are in the "([^"]+)" table:')
def add_rows(self, model_name):
    for row in guess_types(self.hashes):
        # Handle Null values
        row = {k: None if not v else v for k, v in row.items()}
        AnnualFullFormatted.objects.create(**row)

@step('a user is authenticated')
def auth_user(self):
    User.objects.create_user('test_user')
    user = User.objects.get(username='test_user')
    world.client.force_authenticate(user=user)

@step('a user requests path "([^"]+)"')
def data_request(self, request_path):
    world.response = world.client.get(request_path)

@step('the following json response is sent:')
def send_response(self):
    response_json_str = world.response.content.decode('utf-8')
    assert response_json_str == self.multiline
