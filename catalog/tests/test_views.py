# catalog/tests/test_views.py
import pytest
from django.urls import reverse
from catalog.models import Product

@pytest.mark.django_db
def test_home_lists_products(client):
    Product.objects.create(name="Pen", price=10, stock=5)
    r = client.get(reverse("home"))
    assert r.status_code == 200
    assert b"Pen" in r.content
