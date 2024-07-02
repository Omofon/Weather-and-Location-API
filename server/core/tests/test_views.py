from django.test import TestCase
import pytest
from django.urls import reverse
from django.test import Client
from django.conf import settings


@pytest.fixture
def client():
    return Client()


def test_hello_view(client, settings):
    settings.GEOIP_PATH = "C:/Users/hp/Desktop/basic webserver/server/geoip"
    response = client.get(reverse("hello"), {"visitor_name": "Mark"})

    assert response.status_code == 200
    data = response.json()
    assert "client_ip" in data
    assert "location" in data
    assert "greeting" in data
    assert "Hello, Mark!" in data["greeting"]


def test_hello_view_no_name(client, settings):
    settings.GEOIP_PATH = "C:/Users/hp/Desktop/basic webserver/server/geoip"
    response = client.get(reverse("hello"))

    assert response.status_code == 200
    data = response.json()
    assert "client_ip" in data
    assert "location" in data
    assert "greeting" in data
    assert "Hello, Guest!" in data["greeting"]
