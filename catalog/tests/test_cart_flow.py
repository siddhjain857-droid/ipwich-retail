import pytest
from django.urls import reverse
from catalog.models import Product

@pytest.mark.django_db
def test_add_and_view_cart(client):
    p = Product.objects.create(name="Pen", price=1.99, stock=10)
    # add via POST with qty=2
    resp = client.post(reverse("add_to_cart", args=[p.pk]), {"qty": 2})
    assert resp.status_code == 302  # redirected to 'cart'
    r = client.get(reverse("cart"))
    assert r.status_code == 200
    assert b"Pen" in r.content
