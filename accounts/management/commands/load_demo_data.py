from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from menu.models import Category, Dish
from news.models import NewsArticle
from about.models import AboutContent
from contact.models import ContactMessage

User = get_user_model()


class Command(BaseCommand):
    help = "Загружает демо-данные для London Grill"

    def handle(self, *args, **options):
        self.stdout.write("Загрузка демо-данных...")

        self._create_users()
        self._create_categories()
        self._create_dishes()
        self._create_news()
        self._create_about()
        self._create_contacts()

        self.stdout.write(self.style.SUCCESS("Готово! Все демо-данные загружены."))

    def _create_users(self):
        if User.objects.filter(username="admin").exists():
            self.stdout.write("  Пользователи уже есть, пропускаем")
            return

        User.objects.create_superuser("admin", "admin@londongrill.com", "admin123")
        User.objects.create_user("user1", "user1@example.com", "user12345")
        User.objects.create_user("waiter", "waiter@londongrill.com", "waiter123")
        self.stdout.write("  Созданы пользователи: admin, user1, waiter")

    def _create_categories(self):
        if Category.objects.exists():
            self.stdout.write("  Категории уже есть, пропускаем")
            return

        categories = [
            {"name": "Закуски", "description": "Лёгкие закуски к вашему столу", "order": 1},
            {"name": "Салаты", "description": "Свежие и сытные салаты", "order": 2},
            {"name": "Супы", "description": "Горячие супы на любой вкус", "order": 3},
            {"name": "Основные блюда", "description": "Сытные блюда из мяса, рыбы и птицы", "order": 4},
            {"name": "Паста", "description": "Домашняя паста и итальянская классика", "order": 5},
            {"name": "Гриль", "description": "Мясо и овощи, приготовленные на открытом огне", "order": 6},
            {"name": "Десерты", "description": "Сладкое завершение трапезы", "order": 7},
            {"name": "Напитки", "description": "Освежающие и горячие напитки", "order": 8},
        ]
        for cat in categories:
            Category.objects.create(**cat)
        self.stdout.write(f"  Создано {len(categories)} категорий")

    def _create_dishes(self):
        if Dish.objects.exists():
            self.stdout.write("  Блюда уже есть, пропускаем")
            return

        cat_map = {c.name: c for c in Category.objects.all()}

        dishes_data = [
            # Закуски (cat_id=1)
            {"category": "Закуски", "name": "Брускетта с томатами", "description": "Тосты из чиабатты с вялеными томатами, базиликом и оливковым маслом", "price": 8.50, "order": 1},
            {"category": "Закуски", "name": "Креветки в кляре", "description": "Хрустящие креветки с соусом сладкий чили и лаймом", "price": 14.90, "order": 2},
            {"category": "Закуски", "name": "Сырная тарелка", "description": "Ассорти из 5 видов сыра с мёдом и орехами", "price": 18.00, "order": 3},
            {"category": "Закуски", "name": "Карпаччо из говядины", "description": "Тонко нарезанная говядина с рукколой и пармезаном", "price": 16.50, "order": 4},

            # Салаты (cat_id=2)
            {"category": "Салаты", "name": "Цезарь с курицей", "description": "Куриное филе, салат романо, пармезан, гренки, соус цезарь", "price": 12.50, "order": 1},
            {"category": "Салаты", "name": "Греческий салат", "description": "Свежие огурцы, томаты, перец, фета, маслины, оливковое масло", "price": 10.90, "order": 2},
            {"category": "Салаты", "name": "Тёплый салат с лососем", "description": "Слабосолёный лосось, авокадо, микс-салат, сладкая горчичная заправка", "price": 16.00, "order": 3},
            {"category": "Салаты", "name": "Нисуаз с тунцом", "description": "Консервированный тунец, яйцо пашот, стручковая фасоль, оливки", "price": 14.50, "order": 4},

            # Супы (cat_id=3)
            {"category": "Супы", "name": "Тыквенный крем-суп", "description": "Нежный суп из запечённой тыквы с кокосовым молоком и тыквенными семечками", "price": 8.90, "order": 1},
            {"category": "Супы", "name": "Борщ с пампушками", "description": "Классический украинский борщ с чесночными пампушками", "price": 9.50, "order": 2},
            {"category": "Супы", "name": "Том-ям с креветками", "description": "Острый тайский суп на кокосовом молоке с креветками и грибами", "price": 13.90, "order": 3},
            {"category": "Супы", "name": "Куриный суп с лапшой", "description": "Лёгкий куриный бульон с домашней лапшой и овощами", "price": 7.50, "order": 4},

            # Основные блюда (cat_id=4)
            {"category": "Основные блюда", "name": "Стейк Рибай", "description": "Мраморная говядина 300 г с розмариновым маслом и овощами гриль", "price": 34.00, "order": 1},
            {"category": "Основные блюда", "name": "Лосось на гриле", "description": "Филе лосося с лимонно-укропным соусом и молодым картофелем", "price": 28.00, "order": 2},
            {"category": "Основные блюда", "name": "Куриная грудка с грибами", "description": "Куриное филе в сливочном соусе с шампиньонами и тимьяном", "price": 18.50, "order": 3},
            {"category": "Основные блюда", "name": "Баранина с мятным соусом", "description": "Каре ягнёнка с мятным желе и запечёнными корнеплодами", "price": 32.00, "order": 4},

            # Паста (cat_id=5)
            {"category": "Паста", "name": "Карбонара", "description": "Спагетти с беконом, яичным желтком и пармезаном", "price": 14.50, "order": 1},
            {"category": "Паста", "name": "Паста с креветками", "description": "Тальятелле с креветками, чесноком и белым вином", "price": 18.00, "order": 2},
            {"category": "Паста", "name": "Лазанья Болоньезе", "description": "Слоёная паста с мясным соусом и бешамелью", "price": 16.50, "order": 3},
            {"category": "Паста", "name": "Равиоли с рикоттой", "description": "Домашние равиоли с рикоттой и шпинатом в томатном соусе", "price": 15.50, "order": 4},

            # Гриль (cat_id=6)
            {"category": "Гриль", "name": "Люля-кебаб из баранины", "description": "Сочные котлеты из баранины на мангале с лавашом и овощами", "price": 16.00, "order": 1},
            {"category": "Гриль", "name": "Свиные рёбра BBQ", "description": "Свиные рёбра в копчёном соусе BBQ с картофелем фри", "price": 22.00, "order": 2},
            {"category": "Гриль", "name": "Куриные крылья", "description": "Хрустящие крылья в остром соусе с сельдереем и блю-чиз", "price": 13.50, "order": 3},
            {"category": "Гриль", "name": "Микс овощей гриль", "description": "Кабачки, баклажаны, перец, томаты с соусом песто", "price": 10.50, "order": 4},

            # Десерты (cat_id=7)
            {"category": "Десерты", "name": "Тирамису", "description": "Классический итальянский десерт с маскарпоне и кофе", "price": 9.00, "order": 1},
            {"category": "Десерты", "name": "Чизкейк Нью-Йорк", "description": "Кремовый чизкейк с ягодным конфитюром", "price": 10.50, "order": 2},
            {"category": "Десерты", "name": "Фондю шоколадное", "description": "Горячий шоколад с фруктами и зефиром на двоих", "price": 14.00, "order": 3},
            {"category": "Десерты", "name": "Панна-котта с манго", "description": "Нежный итальянский десерт с манговым пюре", "price": 8.50, "order": 4},

            # Напитки (cat_id=8)
            {"category": "Напитки", "name": "Эспрессо", "description": "Классический итальянский эспрессо двойной прожарки", "price": 3.50, "order": 1},
            {"category": "Напитки", "name": "Капучино", "description": "Эспрессо с нежной молочной пеной и корицей", "price": 4.50, "order": 2},
            {"category": "Напитки", "name": "Лимонад маракуйя-имбирь", "description": "Домашний лимонад с маракуйей и свежим имбирём", "price": 5.50, "order": 3},
            {"category": "Напитки", "name": "Мятный чай", "description": "Свежий чай с мятой, мёдом и лаймом", "price": 4.00, "order": 4},
            {"category": "Напитки", "name": "Апероль Шприц", "description": "Игристое вино с Аперолем и апельсином", "price": 8.50, "order": 5},
            {"category": "Напитки", "name": "Красное вино бокал", "description": "Домашнее красное вино (Италия, 2022)", "price": 7.00, "order": 6},
        ]

        for d in dishes_data:
            Dish.objects.create(
                category=cat_map[d["category"]],
                name=d["name"],
                description=d["description"],
                price=d["price"],
                is_available=random.random() > 0.15,
                order=d["order"],
            )
        self.stdout.write(f"  Создано {len(dishes_data)} блюд")

    def _create_news(self):
        if NewsArticle.objects.exists():
            self.stdout.write("  Новости уже есть, пропускаем")
            return

        now = timezone.now()
        news_data = [
            {
                "title": "Новое сезонное меню от шефа",
                "content": "Шеф-повар London Grill представляет новое сезонное меню. Вас ждут блюда из свежих фермерских продуктов, вдохновлённые средиземноморской кухней. Особое внимание уделено сочетанию традиционных рецептов с современными гастрономическими трендами. Приходите и оцените новые вкусы!\n\nВ новом меню: ризотто с белыми грибами, тартар из тунца с авокадо, мусс из чёрного шоколада с морской солью и многое другое.",
                "created_at": now - timedelta(days=2),
                "is_published": True,
            },
            {
                "title": "Дегустационный сет — идеальный ужин",
                "content": "Теперь вы можете попробовать все хиты London Grill в одном сете! Дегустационный сет из 6 подач — идеальный выбор для тех, кто хочет познакомиться с нашей кухней. В сете собраны лучшие блюда, от закусок до десертов, каждое сопровождается рекомендацией сомелье.\n\nСтоимость сета — 4500 сом. Действует при заказе от двух персон. Бронируйте столик заранее!",
                "created_at": now - timedelta(days=6),
                "is_published": True,
            },
            {
                "title": "Субботний бранч — теперь и у нас",
                "content": "Каждую субботу с 11:00 до 15:00 London Grill приглашает на бранч. Свежая выпечка, яичные блюда, салаты, напитки и десерты — всё включено. Дети до 7 лет бесплатно.\n\nСтоимость: 2000 сом на человека. Ждём вас с семьёй и друзьями!",
                "created_at": now - timedelta(days=10),
                "is_published": True,
            },
            {
                "title": "Новый формат доставки — London Box",
                "content": "Мы запустили London Box — готовые наборы для приготовления дома. Всё, что нужно для идеального ужина: продукты, рецепт и видеоинструкция от нашего шефа. Выбирайте бокс на 2 или 4 персоны.\n\nДоставка по городу — бесплатно при заказе от 2500 сом.",
                "created_at": now - timedelta(days=20),
                "is_published": True,
            },
            {
                "title": "London Grill в рейтинге лучших ресторанов города",
                "content": "Мы рады сообщить, что London Grill вошёл в топ-10 ресторанов города по версии престижного ресторанного гида. Это признание нашей работы и любви к гостям. Спасибо, что выбираете нас!\n\nОсобая благодарность нашей команде — без вас это было бы невозможно.",
                "created_at": now - timedelta(days=35),
                "is_published": True,
            },
        ]
        for n in news_data:
            NewsArticle.objects.create(**n)
        self.stdout.write(f"  Создано {len(news_data)} новостей")

    def _create_about(self):
        if AboutContent.objects.exists():
            self.stdout.write("  Информация 'О нас' уже есть, пропускаем")
            return

        AboutContent.objects.create(
            title="Добро пожаловать в London Grill",
            content=(
                "London Grill — это не просто ресторан. Это место, где встречаются традиции английской кухни и "
                "современные гастрономические тенденции. Наш шеф-повар с 15-летним опытом лично отбирает продукты "
                "на локальных рынках, чтобы каждое блюдо было свежим и неповторимым.\n\n"
                "Мы гордимся уютной атмосферой, внимательным сервисом и, конечно, нашей открытой кухней — "
                "вы всегда видите, как рождаются ваши любимые блюда.\n\n"
                "Интерьер ресторана сочетает классический британский стиль с современными акцентами. "
                "У нас есть уютный зал на 50 мест, летняя терраса и отдельный VIP-зал для частных мероприятий.\n\n"
                "Ждём вас каждый день с 08:00 до 00:00. Бронирование столов по телефону +1 212-344-1230."
            ),
        )
        self.stdout.write("  Создана информация 'О нас'")

    def _create_contacts(self):
        if ContactMessage.objects.exists():
            self.stdout.write("  Контактные сообщения уже есть, пропускаем")
            return

        messages = [
            {"name": "Анна", "email": "anna@example.com", "message": "Добрый день! Хотим забронировать столик на 25 декабря на 4 человека. Есть ли свободные места?", "is_read": True},
            {"name": "Марат", "email": "marat@example.com", "message": "Подскажите, есть ли у вас вегетарианское меню? Я планирую прийти с друзьями в пятницу.", "is_read": True},
            {"name": "Елена", "email": "elena@example.com", "message": "Очень понравился ваш ресторан! Особенно десерты — тирамису просто божественный. Обязательно придём ещё!", "is_read": False},
        ]
        for m in messages:
            ContactMessage.objects.create(**m)
        self.stdout.write(f"  Создано {len(messages)} контактных сообщений")
