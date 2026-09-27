from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import MenuCategory, MenuItem, StoreLocation, Feature, Order, OrderItem
from .cart import Cart


def home(request):
    categories = MenuCategory.objects.prefetch_related("items").all()
    featured = MenuItem.objects.filter(is_available=True, is_featured=True)[:6]
    stores = StoreLocation.objects.all()
    features = Feature.objects.all()
    return render(request, "menu/home.html", {
        "categories": categories,
        "featured": featured,
        "stores": stores,
        "features": features,
    })


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    cart.add(item, quantity=1)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True, "cart_count": len(cart), "item_name": item.name})

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "home"
    return redirect(next_url)


@require_POST
def cart_update(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, id=item_id)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1
    cart.set_quantity(item, quantity)
    return redirect("cart_detail")


@require_POST
def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, id=item_id)
    cart.remove(item)
    return redirect("cart_detail")


def cart_detail(request):
    cart = Cart(request)
    return render(request, "menu/cart.html", {"cart": cart})


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("cart_detail")

    error = None
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        note = request.POST.get("note", "").strip()

        if full_name and phone:
            order = Order.objects.create(
                full_name=full_name, phone=phone, address=address, note=note,
            )
            for row in cart:
                OrderItem.objects.create(
                    order=order,
                    product=row["item"],
                    product_name=row["item"].name,
                    quantity=row["quantity"],
                    price=row["item"].price,
                )
            cart.clear()
            return redirect("order_success", order_id=order.id)
        error = "Вкажіть, будь ласка, ім'я та телефон."

    return render(request, "menu/checkout.html", {"cart": cart, "error": error})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "menu/order_success.html", {"order": order})
