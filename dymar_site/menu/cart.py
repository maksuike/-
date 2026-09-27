from .models import MenuItem

CART_SESSION_KEY = "cart"


class Cart:
    """Simple session-based cart: {item_id (str): {"quantity": int}}"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, item, quantity=1):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {"quantity": 0}
        self.cart[item_id]["quantity"] += quantity
        self.save()

    def set_quantity(self, item, quantity):
        item_id = str(item.id)
        if quantity <= 0:
            self.remove(item)
            return
        self.cart[item_id] = {"quantity": quantity}
        self.save()

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def _items_map(self):
        ids = self.cart.keys()
        return {str(i.id): i for i in MenuItem.objects.filter(id__in=ids)}

    def __iter__(self):
        items_map = self._items_map()
        for item_id, data in list(self.cart.items()):
            item = items_map.get(item_id)
            if not item:
                continue
            yield {
                "item": item,
                "quantity": data["quantity"],
                "subtotal": item.price * data["quantity"],
            }

    def __len__(self):
        return sum(d["quantity"] for d in self.cart.values())

    def get_total_price(self):
        return sum(row["subtotal"] for row in self)
