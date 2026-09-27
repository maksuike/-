from django.core.management.base import BaseCommand
from menu.models import MenuCategory, MenuItem, StoreLocation, Feature

CATEGORIES = {
    "Копченості": [
        ("Рвана свинина", "100 г", 48, True),
        ("Ребра копчені в смокері", "100 г", 60, True),
        ("Підчеревина копчена", "100 г", 48, False),
        ("Копчена ковбаса домашня", "100 г", 52, False),
    ],
    "BBQ": [
        ("Рвана яловичина", "100 г", 75, True),
        ("Рулет курячий BBQ", "100 г", 78, True),
        ("Крильця BBQ", "100 г", 42, False),
    ],
    "Мариноване м'ясо": [
        ("Шия свиняча в маринаді", "1 кг", 320, False),
        ("Стегно куряче в маринаді", "1 кг", 210, False),
        ("Реберця свинячі в маринаді", "1 кг", 290, False),
    ],
    "Сиров'ялена продукція": [
        ("Бастурма яловича", "100 г", 145, False),
        ("Прошутто свиняче", "100 г", 130, False),
    ],
    "Соуси і спеції": [
        ("Соус BBQ домашній", "200 мл", 65, False),
        ("Суха суміш для брискету", "100 г", 55, False),
    ],
    "М'ясні набори": [
        ("Набір «Компанія» на 4 особи", "~1.6 кг", 890, True),
    ],
}

FEATURES = [
    ("Свіжа та якісна продукція", "Готуємо щодня невеликими партіями — лише перевірена сировина від надійних постачальників."),
    ("Доставка по області", "Розвозимо замовлення з трьох магазинів — приїде свіжим і вчасно."),
    ("Чесна ціна", "Якість без переплати: ціна відповідає продукту, асортимент — під будь-який бюджет."),
    ("Широкий асортимент", "Яловичина, свинина, птиця, копченості та BBQ — все в одному місці."),
]

STORES = [
    ("Центральний", "вул. Головна, 12", "09:00–20:00", "+380 99 123 45 67"),
    ("Кіцмань", "вул. Незалежності, 54А", "09:00–20:00", "050 140 88 80"),
    ("Остриця", "вул. Чернівецька, 20", "09:00–19:00", "066 212 88 80"),
]


class Command(BaseCommand):
    help = "Наповнює базу стартовим асортиментом, перевагами й магазинами ДИМАР"

    def handle(self, *args, **options):
        if MenuCategory.objects.exists():
            self.stdout.write("Асортимент вже наповнений — пропускаю.")
        else:
            for order, (cat_name, items) in enumerate(CATEGORIES.items()):
                cat = MenuCategory.objects.create(name=cat_name, order=order)
                for i_order, (name, unit, price, featured) in enumerate(items):
                    MenuItem.objects.create(
                        category=cat, name=name, unit=unit, price=price,
                        is_featured=featured, order=i_order,
                    )
            self.stdout.write(self.style.SUCCESS("Асортимент створено."))

        if not Feature.objects.exists():
            for order, (title, text) in enumerate(FEATURES):
                Feature.objects.create(title=title, text=text, order=order)
            self.stdout.write(self.style.SUCCESS("Переваги створено."))

        if not StoreLocation.objects.exists():
            for order, (name, address, hours, phone) in enumerate(STORES):
                StoreLocation.objects.create(
                    name=name, address=address, hours=hours, phone=phone, order=order,
                )
            self.stdout.write(self.style.SUCCESS("Магазини створено."))
