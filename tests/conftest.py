import json

import pytest
from django.contrib.auth import get_user_model
from mfa.models import User_Keys

@pytest.mark.django_db
def create_user(username, password, is_staff, email=None):
    user = get_user_model().objects.create_user(username=username, password=password)
    user.is_staff = is_staff
    if email:
        user.email = email
    user.save()
    return user


@pytest.mark.django_db
def create_mfa_entries(username):

    file_path = "tests/fixtures/dj_rest_auth_mfa_mfa2_user_keys_dump.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        item["username"] = username

    objects = [User_Keys(**item) for item in data]
    User_Keys.objects.bulk_create(objects)

    return True


@pytest.fixture(scope="function")
def unauthenticated_api_client(request):
    # What about drf-mongoengine
    from rest_framework.test import APIClient

    client = APIClient()
    # tox fails without the following client.get()
    # without it the next client.get(url)...
    # will result in 404 regardless of the url
    # it seems like it is an initialization issue maybe
    # of client.requests and not of the client itself.
    response = client.get("")
    assert response.status_code == 403
    yield client
