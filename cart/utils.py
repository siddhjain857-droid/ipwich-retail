from decimal import Decimal


class SessionCart:
    KEY = "cart_items"


    def __init__(self, request):
        self.session = request.session
        self.items = self.session.get(self.KEY, {})


    def add(self, product_id, price, qty=1):
        pid = str(product_id)
        item = self.items.get(pid, {"qty": 0, "price": str(price)})
        item["qty"] += qty
        self.items[pid] = item
        self._save()


    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.items:
            del self.items[pid]
            self._save()


    def update(self, product_id, qty):
        pid = str(product_id)
        if pid in self.items:
            self.items[pid]["qty"] = int(qty)
            self._save()


    def clear(self):
        self.session[self.KEY] = {}
        self.session.modified = True


    def total(self):
        return sum(Decimal(v["price"]) * v["qty"] for v in self.items.values())


    def _save(self):
        self.session[self.KEY] = self.items
        self.session.modified = True