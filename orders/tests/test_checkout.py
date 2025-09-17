# orders/tests/test_checkout.py
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from catalog.models import Product

@pytest.mark.django_db
def test_checkout_creates_order(client):
    u = User.objects.create_user("demo","demo@example.com","pass")
    client.login(username="demo", password="pass")
    p = Product.objects.create(name="Notebook", price=50, stock=10)
    session = client.session
    session["cart"] = {str(p.id): 2}
    session.save()
    r = client.post(reverse("checkout"))
    assert r.status_code == 302  # redirect to confirmation