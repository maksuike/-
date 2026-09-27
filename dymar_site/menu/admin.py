from django.contrib import admin
from django.utils.html import format_html
from .models import MenuCategory, MenuItem, StoreLocation, Feature, Order, OrderItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ("name", "unit", "price", "image", "is_available", "is_featured", "order")


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "category", "unit", "price", "is_available", "is_featured", "order")
    list_filter = ("category", "is_available", "is_featured")
    list_editable = ("price", "is_available", "is_featured", "order")

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:4px;">', obj.image.url)
        return "—"
    thumb.short_description = "Фото"


@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "hours", "phone", "order")
    list_editable = ("address", "hours", "phone", "order")


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "order")
    list_editable = ("text", "order")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "quantity", "price")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "status", "total_display", "created_at")
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    readonly_fields = ("full_name", "phone", "address", "note", "created_at")
    inlines = [OrderItemInline]

    def total_display(self, obj):
        return f"{obj.total()} ₴"
    total_display.short_description = "Сума"
