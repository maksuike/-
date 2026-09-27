from django.db import models


class MenuCategory(models.Model):
    name = models.CharField("Назва категорії", max_length=80)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Категорія товарів"
        verbose_name_plural = "Категорії товарів"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        MenuCategory, related_name="items", on_delete=models.CASCADE,
        verbose_name="Категорія",
    )
    name = models.CharField("Назва товару", max_length=120)
    unit = models.CharField("Фасування", max_length=40, default="100 г")
    price = models.DecimalField("Ціна, грн", max_digits=7, decimal_places=0)
    image = models.ImageField("Фото товару", upload_to="products/", blank=True, null=True)
    is_available = models.BooleanField("В наявності", default=True)
    is_featured = models.BooleanField("Топ продажів", default=False)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} — {self.price} ₴"


class StoreLocation(models.Model):
    name = models.CharField("Назва магазину", max_length=80)
    address = models.CharField("Адреса", max_length=160)
    hours = models.CharField("Графік роботи", max_length=60)
    phone = models.CharField("Телефон", max_length=30)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазини"
        ordering = ["order"]

    def __str__(self):
        return self.name


class Feature(models.Model):
    title = models.CharField("Заголовок", max_length=80)
    text = models.CharField("Опис", max_length=200)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        verbose_name = "Перевага"
        verbose_name_plural = "Чому обирають нас"
        ordering = ["order"]

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Нове"),
        ("confirmed", "Підтверджено"),
        ("done", "Виконано"),
    ]
    full_name = models.CharField("Ім'я", max_length=120)
    phone = models.CharField("Телефон", max_length=30)
    address = models.CharField("Адреса доставки", max_length=200, blank=True)
    note = models.CharField("Коментар", max_length=300, blank=True)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Замовлення #{self.id} — {self.full_name}"

    def total(self):
        return sum(i.subtotal() for i in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField("Назва товару", max_length=120)
    quantity = models.PositiveIntegerField("Кількість", default=1)
    price = models.DecimalField("Ціна за од., грн", max_digits=7, decimal_places=0)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"
