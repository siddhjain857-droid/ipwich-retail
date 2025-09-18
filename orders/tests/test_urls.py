# orders/tests/test_urls.py
from django.urls import reverse

def test_urls_resolve():
    assert reverse("checkout") == "/orders/checkout/"
    assert reverse("order_confirmation", kwargs={"order_id": 123}) == "/orders/confirmation/123/"
    assert reverse("my_orders") == "/orders/"