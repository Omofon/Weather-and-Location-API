import pytest
from django.urls import reverse, resolve
from core.views import hello


def test_hello_url():
    path = reverse("hello")
    assert resolve(path).func == hello
