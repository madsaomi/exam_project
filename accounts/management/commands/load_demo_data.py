from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from menu.models import Category, Dish, Testimonial
from news.models import NewsArticle
from about.models import AboutContent
from contact.models import ContactMessage

User = get_user_model()

TR = {
    'en': 'en', 'ru': 'ru', 'uz': 'uz',
}


def t(name_ru, name_en, name_uz, desc_ru='', desc_en='', desc_uz=''):
    return {
        'ru': {'name': name_ru, 'description': desc_ru},
        'en': {'name': name_en, 'description': desc_en},
        'uz': {'name': name_uz, 'description': desc_uz},
    }


class Command(BaseCommand):
    help = "Loads demo data with EN/RU/UZ translations"

    def handle(self, *args, **options):
        self.stdout.write("Loading demo data...")
        self._create_users()
        self._create_categories()
        self._create_dishes()
        self._create_news()
        self._create_testimonials()
        self._create_about()
        self._create_contacts()
        self._download_images()
        self.stdout.write(self.style.SUCCESS("Done! All demo data loaded."))

    def _create_users(self):
        if User.objects.filter(username="admin").exists():
            self.stdout.write("  Users exist, skipping")
            return
        User.objects.create_superuser("admin", "admin@londongrill.com", "admin123")
        User.objects.create_user("user1", "user1@example.com", "user12345")
        User.objects.create_user("waiter", "waiter@londongrill.com", "waiter123")
        self.stdout.write("  Created: admin, user1, waiter")

    def _create_categories(self):
        if Category.objects.exists():
            self.stdout.write("  Categories exist, skipping")
            return
        cats = [
            {"name": "Закуски", "translations": t("Закуски", "Appetizers", "Aperitivlar",
                "Лёгкие закуски к вашему столу", "Light appetizers for your table", "Engil atirliklar")},
            {"name": "Салаты", "translations": t("Салаты", "Salads", "Salatlar",
                "Свежие и сытные салаты", "Fresh and hearty salads", "Yangi va to'yingan salatlar")},
            {"name": "Супы", "translations": t("Супы", "Soups", "Sho'rvalar",
                "Горячие супы на любой вкус", "Hot soups for every taste", "Har qanday ta'mga issiq sho'rvalar")},
            {"name": "Основные блюда", "translations": t("Основные блюда", "Main Courses", "Asosiy taomlar",
                "Сытные блюда из мяса, рыбы и птицы", "Hearty meat, fish and poultry dishes", "Go'sht, baliq va parranda taomlari")},
            {"name": "Паста", "translations": t("Паста", "Pasta", "Pasta",
                "Домашняя паста и итальянская классика", "Homemade pasta and Italian classics", "Uy qurilishi pasta va italyan klassikasi")},
            {"name": "Гриль", "translations": t("Гриль", "Grill", "Grill",
                "Мясо и овощи на открытом огне", "Meat and vegetables over an open fire", "Ochiq olovda go'sht va sabzavotlar")},
            {"name": "Десерты", "translations": t("Десерты", "Desserts", "Shirinliklar",
                "Сладкое завершение трапезы", "Sweet ending to your meal", "Taomning shirin yakuni")},
            {"name": "Напитки", "translations": t("Напитки", "Drinks", "Ichimliklar",
                "Освежающие и горячие напитки", "Refreshing and hot drinks", "Tetiklantiruvchi va issiq ichimliklar")},
        ]
        for i, c in enumerate(cats):
            Category.objects.create(name=c["name"], translations=c["translations"], order=i + 1)
        self.stdout.write(f"  Created {len(cats)} categories")

    def _create_dishes(self):
        if Dish.objects.exists():
            self.stdout.write("  Dishes exist, skipping")
            return
        cat_map = {c.name: c for c in Category.objects.all()}

        dishes_data = [
            ("Закуски", "Брускетта с томатами", "Bruschetta with Tomatoes", "Brusketta pomidor bilan",
             "Тосты из чиабатты с вялеными томатами, базиликом и оливковым маслом",
             "Ciabatta toasts with sun-dried tomatoes, basil and olive oil",
             "Quyida quritilgan pomidor, rayhon va zaytun moyi bilan chabatta tostlari", 8.50),
            ("Закуски", "Креветки в кляре", "Battered Shrimp", "Xamirda qisqichbaqalar",
             "Хрустящие креветки с соусом сладкий чили и лаймом",
             "Crispy shrimp with sweet chili sauce and lime",
             "Shirin chili sousi va laym bilan qarsildoq qisqichbaqalar", 14.90),
            ("Закуски", "Сырная тарелка", "Cheese Plate", "Pishloq taxtasi",
             "Ассорти из 5 видов сыра с мёдом и орехами",
             "Selection of 5 cheeses with honey and nuts",
             "Asal va yong'oq bilan 5 turdagi pishloq assorti", 18.00),
            ("Закуски", "Карпаччо из говядины", "Beef Carpaccio", "Mol go'shti karpaççosi",
             "Тонко нарезанная говядина с рукколой и пармезаном",
             "Thinly sliced beef with arugula and parmesan",
             "Rukola va parmezan bilan yupqa kesilgan mol go'shti", 16.50),
            ("Салаты", "Цезарь с курицей", "Chicken Caesar", "Tovuqli Sezar",
             "Куриное филе, салат романо, пармезан, гренки, соус цезарь",
             "Chicken fillet, romaine lettuce, parmesan, croutons, caesar dressing",
             "Tovuq filesi, romain salati, parmezan, krutonlar, sezar sousi", 12.50),
            ("Салаты", "Греческий салат", "Greek Salad", "Gretsiya salati",
             "Огурцы, томаты, перец, фета, маслины, оливковое масло",
             "Cucumbers, tomatoes, peppers, feta, olives, olive oil",
             "Bodring, pomidor, qalampir, feta, zaytun, zaytun moyi", 10.90),
            ("Салаты", "Тёплый салат с лососем", "Warm Salmon Salad", "Issiq losos salati",
             "Слабосолёный лосось, авокадо, микс-салат, горчичная заправка",
             "Lightly salted salmon, avocado, mixed greens, mustard dressing",
             "Yengil tuzlangan losos, avokado, aralash salat, xantal sousi", 16.00),
            ("Салаты", "Нисуаз с тунцом", "Niçoise with Tuna", "Tunets bilan Nisua",
             "Тунец, яйцо пашот, стручковая фасоль, оливки",
             "Tuna, poached egg, green beans, olives",
             "Tunets, poshe tuxum, yashil loviya, zaytun", 14.50),
            ("Супы", "Тыквенный крем-суп", "Pumpkin Cream Soup", "Qovoqli krem sho'rva",
             "Нежный суп из запечённой тыквы с кокосовым молоком и семечками",
             "Smooth roasted pumpkin soup with coconut milk and seeds",
             "Kokos suti va urug'lar bilan qovurilgan qovoq sho'rvasi", 8.90),
            ("Супы", "Борщ с пампушками", "Borscht with Garlic Buns", "Pampushkali borsh",
             "Классический украинский борщ с чесночными пампушками",
             "Classic Ukrainian borscht with garlic buns",
             "Sarimsoq bulochkalar bilan klassik ukrain borshi", 9.50),
            ("Супы", "Том-ям с креветками", "Tom Yum with Shrimp", "Qisqichbaqalar bilan Tom Yam",
             "Острый тайский суп на кокосовом молоке с креветками и грибами",
             "Spicy Thai coconut soup with shrimp and mushrooms",
             "Qisqichbaqalar va qo'ziqorinlar bilan achchiq Tailand kokos sho'rvasi", 13.90),
            ("Супы", "Куриный суп с лапшой", "Chicken Noodle Soup", "Tovuqli noodle sho'rva",
             "Лёгкий куриный бульон с домашней лапшой и овощами",
             "Light chicken broth with homemade noodles and vegetables",
             "Uy qurilishi noodle va sabzavotlar bilan engil tovuq buloni", 7.50),
            ("Основные блюда", "Стейк Рибай", "Ribeye Steak", "Ribeye Steyk",
             "Мраморная говядина 300 г с розмариновым маслом и овощами гриль",
             "300g marbled beef with rosemary oil and grilled vegetables",
             "300g marmar mol go'shti rozmarin yog'i va gril sabzavotlar bilan", 34.00),
            ("Основные блюда", "Лосось на гриле", "Grilled Salmon", "Gril losos",
             "Филе лосося с лимонно-укропным соусом и молодым картофелем",
             "Salmon fillet with lemon-dill sauce and young potatoes",
             "Limon-arpabodiyon sousi va yosh kartoshka bilan losos filesi", 28.00),
            ("Основные блюда", "Куриная грудка с грибами", "Chicken Breast with Mushrooms", "Qo'ziqorinli tovuq ko'kragi",
             "Куриное филе в сливочном соусе с шампиньонами и тимьяном",
             "Chicken fillet in cream sauce with mushrooms and thyme",
             "Qaymoqli sousda shampinyonlar va timyan bilan tovuq filesi", 18.50),
            ("Основные блюда", "Баранина с мятным соусом", "Lamb with Mint Sauce", "Yalpiz sousli qo'y go'shti",
             "Каре ягнёнка с мятным желе и запечёнными корнеплодами",
             "Lamb rack with mint jelly and roasted root vegetables",
             "Yalpiz jeli va qovurilgan ildiz sabzavotlar bilan qo'y go'shti", 32.00),
            ("Паста", "Карбонара", "Carbonara", "Karbonara",
             "Спагетти с беконом, яичным желтком и пармезаном",
             "Spaghetti with bacon, egg yolk and parmesan",
             "Bekon, tuxum sarig'i va parmezan bilan spagetti", 14.50),
            ("Паста", "Паста с креветками", "Shrimp Pasta", "Qisqichbaqalar bilan pasta",
             "Тальятелле с креветками, чесноком и белым вином",
             "Tagliatelle with shrimp, garlic and white wine",
             "Qisqichbaqalar, sarimsoq va oq sharob bilan talyatelyoni", 18.00),
            ("Паста", "Лазанья Болоньезе", "Lasagna Bolognese", "Lasanya Bolonyez",
             "Слоёная паста с мясным соусом и бешамелью",
             "Layered pasta with meat sauce and béchamel",
             "Go'sht sousi va beshamel bilan qatlamli pasta", 16.50),
            ("Паста", "Равиоли с рикоттой", "Ravioli with Ricotta", "Rikotta bilan raviolli",
             "Домашние равиоли с рикоттой и шпинатом в томатном соусе",
             "Homemade ravioli with ricotta and spinach in tomato sauce",
             "Pomidor sousida rikotta va ismaloq bilan uy qurilishi raviollisi", 15.50),
            ("Гриль", "Люля-кебаб из баранины", "Lamb Lyulya-Kebab", "Qo'y go'shtidan lyulya-kabob",
             "Сочные котлеты из баранины на мангале с лавашом и овощами",
             "Juicy lamb patties on charcoal with lavash and vegetables",
             "Lavash va sabzavotlar bilan ko'mirda qovurilgan qo'y go'shti kotletlari", 16.00),
            ("Гриль", "Свиные рёбра BBQ", "BBQ Pork Ribs", "BBQ cho'chqa qovurg'alari",
             "Свиные рёбра в копчёном соусе BBQ с картофелем фри",
             "Pork ribs in smoky BBQ sauce with french fries",
             "Fri kartoshka bilan dudlangan BBQ sousida cho'chqa qovurg'alari", 22.00),
            ("Гриль", "Куриные крылья", "Chicken Wings", "Tovuq qanotchalari",
             "Хрустящие крылья в остром соусе с сельдереем и блю-чиз",
             "Crispy wings in hot sauce with celery and blue cheese",
             "Selderey va blue cheese bilan achchiq sousda qarsildoq qanotchalar", 13.50),
            ("Гриль", "Микс овощей гриль", "Mixed Grilled Vegetables", "Gril sabzavotlar assortisi",
             "Кабачки, баклажаны, перец, томаты с соусом песто",
             "Zucchini, eggplant, peppers, tomatoes with pesto sauce",
             "Pesto sousi bilan qovoq, baqlajon, qalampir, pomidor", 10.50),
            ("Десерты", "Тирамису", "Tiramisu", "Tiramisu",
             "Классический итальянский десерт с маскарпоне и кофе",
             "Classic Italian dessert with mascarpone and coffee",
             "Maskarpone va qahva bilan klassik italyan shirinligi", 9.00),
            ("Десерты", "Чизкейк Нью-Йорк", "New York Cheesecake", "Nyu-York cheeskeyki",
             "Кремовый чизкейк с ягодным конфитюром",
             "Creamy cheesecake with berry confit",
             "Rezavor konfit bilan kremli cheeskeyk", 10.50),
            ("Десерты", "Фондю шоколадное", "Chocolate Fondue", "Shokoladli fondyu",
             "Горячий шоколад с фруктами и зефиром на двоих",
             "Hot chocolate with fruits and marshmallows for two",
             "Ikki kishilik mevalar va marshmallow bilan issiq shokolad", 14.00),
            ("Десерты", "Панна-котта с манго", "Panna Cotta with Mango", "Mango bilan panna-kotta",
             "Нежный итальянский десерт с манговым пюре",
             "Smooth Italian dessert with mango puree",
             "Mango pyuresi bilan mayin italyan shirinligi", 8.50),
            ("Напитки", "Эспрессо", "Espresso", "Espresso",
             "Классический итальянский эспрессо двойной прожарки",
             "Classic Italian double-roast espresso",
             "Klassik italyan ikki marta qovurilgan espresso", 3.50),
            ("Напитки", "Капучино", "Cappuccino", "Kapuchino",
             "Эспрессо с нежной молочной пеной и корицей",
             "Espresso with velvety milk foam and cinnamon",
             "Dolchin bilan mayin sut ko'pikli espresso", 4.50),
            ("Напитки", "Лимонад маракуйя-имбирь", "Passion Fruit Ginger Lemonade", "Passionfruit zanjabil limonadi",
             "Домашний лимонад с маракуйей и свежим имбирём",
             "Homemade lemonade with passion fruit and fresh ginger",
             "Passionfruit va yangi zanjabil bilan uy qurilishi limonadi", 5.50),
            ("Напитки", "Мятный чай", "Mint Tea", "Yalpiz choyi",
             "Свежий чай с мятой, мёдом и лаймом",
             "Fresh tea with mint, honey and lime",
             "Yalpiz, asal va laym bilan yangi choy", 4.00),
            ("Напитки", "Апероль Шприц", "Aperol Spritz", "Aperol Shprits",
             "Игристое вино с Аперолем и апельсином",
             "Sparkling wine with Aperol and orange",
             "Aperol va apelsin bilan gazlangan vino", 8.50),
            ("Напитки", "Красное вино бокал", "Red Wine Glass", "Qizil vino stakan",
             "Домашнее красное вино (Италия, 2022)",
             "House red wine (Italy, 2022)",
             "Uy qizil vinosi (Italiya, 2022)", 7.00),
        ]

        for cat_name, name_ru, name_en, name_uz, desc_ru, desc_en, desc_uz, price in dishes_data:
            Dish.objects.create(
                category=cat_map[cat_name],
                name=name_ru,
                price=price,
                is_available=random.random() > 0.15,
                translations={
                    'ru': {'name': name_ru, 'description': desc_ru},
                    'en': {'name': name_en, 'description': desc_en},
                    'uz': {'name': name_uz, 'description': desc_uz},
                }
            )
        self.stdout.write(f"  Created {len(dishes_data)} dishes")

    def _create_news(self):
        if NewsArticle.objects.exists():
            self.stdout.write("  News exist, skipping")
            return
        now = timezone.now()
        news_data = [
            {
                "title": "Новое сезонное меню от шефа",
                "created_at": now - timedelta(days=2),
                "translations": {
                    "ru": {"title": "Новое сезонное меню от шефа", "content": "Шеф-повар London Grill представляет новое сезонное меню. Вас ждут блюда из свежих фермерских продуктов, вдохновлённые средиземноморской кухней. Особое внимание уделено сочетанию традиционных рецептов с современными гастрономическими трендами."},
                    "en": {"title": "New Seasonal Menu from the Chef", "content": "London Grill's chef presents a new seasonal menu. Fresh farm products inspired by Mediterranean cuisine. Traditional recipes meet modern gastronomic trends."},
                    "uz": {"title": "Oshpazdan yangi mavsumiy menyu", "content": "London Grill oshpazi yangi mavsumiy menyuni taqdim etadi. O'rta er dengizi oshxonasidan ilhomlangan yangi fermer mahsulotlari. An'anaviy retseptlar zamonaviy gastronomik tendentsiyalar bilan uchrashadi."},
                },
            },
            {
                "title": "Дегустационный сет — идеальный ужин",
                "created_at": now - timedelta(days=6),
                "translations": {
                    "ru": {"title": "Дегустационный сет — идеальный ужин", "content": "Попробуйте все хиты London Grill в одном сете! Дегустационный сет из 6 подач — идеальный выбор для знакомства с нашей кухней. Лучшие блюда от закусок до десертов с рекомендациями сомелье."},
                    "en": {"title": "Tasting Set — The Perfect Dinner", "content": "Try all London Grill hits in one set! A 6-course tasting set — perfect for getting to know our cuisine. Best dishes from appetizers to desserts with sommelier recommendations."},
                    "uz": {"title": "Degustatsion set — mukammal kechki ovqat", "content": "London Grill hitlarini bitta setda sinab ko'ring! 6 ta taomdan iborat degustatsion set — oshxonamiz bilan tanishish uchun mukammal tanlov. Somelye tavsiyalari bilan atirliklardan shirinlikkacha eng yaxshi taomlar."},
                },
            },
            {
                "title": "Субботний бранч — теперь и у нас",
                "created_at": now - timedelta(days=10),
                "translations": {
                    "ru": {"title": "Субботний бранч — теперь и у нас", "content": "Каждую субботу с 11:00 до 15:00 London Grill приглашает на бранч. Свежая выпечка, яичные блюда, салаты, напитки и десерты — всё включено. Дети до 7 лет бесплатно."},
                    "en": {"title": "Saturday Brunch — Now at Our Place", "content": "Every Saturday 11:00-15:00 London Grill invites you to brunch. Fresh pastries, egg dishes, salads, drinks and desserts — all included. Children under 7 free."},
                    "uz": {"title": "Shanba kungi brunch — endi bizda", "content": "Har shanba kuni soat 11:00-15:00 gacha London Grill brunchga taklif qiladi. Yangi pishiriqlar, tuxumli taomlar, salatlar, ichimliklar va shirinliklar — hammasi kiritilgan. 7 yoshgacha bolalar bepul."},
                },
            },
            {
                "title": "Новый формат доставки — London Box",
                "created_at": now - timedelta(days=20),
                "translations": {
                    "ru": {"title": "Новый формат доставки — London Box", "content": "Мы запустили London Box — готовые наборы для приготовления дома. Всё для идеального ужина: продукты, рецепт и видеоинструкция от шефа. Выбирайте бокс на 2 или 4 персоны."},
                    "en": {"title": "New Delivery Format — London Box", "content": "We launched London Box — ready-to-cook meal kits. Everything for the perfect dinner: ingredients, recipe and video guide from the chef. Choose a box for 2 or 4 people."},
                    "uz": {"title": "Yetkazib berishning yangi formati — London Box", "content": "Biz London Box — uyda tayyorlash uchun tayyor to'plamlarni ishga tushirdik. Mukammal kechki ovqat uchun: mahsulotlar, retsept va oshpazdan video ko'rsatma. 2 yoki 4 kishiga boxni tanlang."},
                },
            },
            {
                "title": "London Grill в рейтинге лучших ресторанов",
                "created_at": now - timedelta(days=35),
                "translations": {
                    "ru": {"title": "London Grill в рейтинге лучших ресторанов", "content": "London Grill вошёл в топ-10 ресторанов города по версии престижного ресторанного гида. Это признание нашей работы и любви к гостям. Спасибо, что выбираете нас!"},
                    "en": {"title": "London Grill in Best Restaurants Rating", "content": "London Grill entered the top 10 restaurants of the city according to a prestigious restaurant guide. This is recognition of our work and love for guests. Thank you for choosing us!"},
                    "uz": {"title": "London Grill eng yaxshi restoranlar reytingida", "content": "London Grill nufuzli restoran qo'llanmasiga ko'ra shaharning eng yaxshi 10 ta restorani qatoriga kirdi. Bu bizning ishimiz va mehmonlarga bo'lgan muhabbatimizning tan olinishi. Bizni tanlaganingiz uchun rahmat!"},
                },
            },
        ]
        for n in news_data:
            content_ru = n["translations"]["ru"]["content"]
            n["content"] = content_ru
            NewsArticle.objects.create(
                title=n["title"],
                content=content_ru,
                created_at=n["created_at"],
                translations=n["translations"],
            )
        self.stdout.write(f"  Created {len(news_data)} news")

    def _create_testimonials(self):
        if Testimonial.objects.exists():
            self.stdout.write("  Testimonials exist, skipping")
            return
        testimonials = [
            {"order": 1, "translations": {
                "en": {"name": "Maria", "text": "A very cozy place with amazing food. The staff is incredibly friendly and the atmosphere is just perfect for a romantic dinner."},
                "ru": {"name": "Мария", "text": "Очень уютное место с потрясающей едой. Персонал невероятно дружелюбный, а атмосфера идеально подходит для романтического ужина."},
                "uz": {"name": "Mariya", "text": "Ajoyib taomlar bilan juda qulay joy. Xodimlar nihoyatda do'stona, atmosfera esa romantik kechki ovqat uchun juda mos."},
            }},
            {"order": 2, "translations": {
                "en": {"name": "James", "text": "I ordered delivery several times and every dish was fresh and delicious. The steak was cooked perfectly. Highly recommended!"},
                "ru": {"name": "Джеймс", "text": "Заказывал доставку несколько раз — каждое блюдо было свежим и вкусным. Стейк приготовлен идеально. Очень рекомендую!"},
                "uz": {"name": "Djeyms", "text": "Bir necha marta yetkazib berishga buyurtma berdim — har bir taom yangi va mazali edi. Steyk mukammal pishirilgan. Tavsiya qilaman!"},
            }},
            {"order": 3, "translations": {
                "en": {"name": "Aisha", "text": "Atmosphere, service and taste — everything was top notch. The grilled salmon is the best I have ever had. Will definitely come back."},
                "ru": {"name": "Аиша", "text": "Атмосфера, сервис и вкус — всё на высшем уровне. Лосось на гриле — лучшее, что я пробовала. Обязательно вернусь."},
                "uz": {"name": "Oysha", "text": "Atmosfera, xizmat va ta'm — hammasi yuqori darajada. Gril losos men tatib ko'rgan eng yaxshisi. Albatta qaytib kelaman."},
            }},
            {"order": 4, "translations": {
                "en": {"name": "Dmitry", "text": "Great selection of wines and the chef's tasting menu is an experience worth having. The tiramisu for dessert is a must-try."},
                "ru": {"name": "Дмитрий", "text": "Отличный выбор вин, а дегустационное меню от шефа — это опыт, который стоит попробовать. Тирамису на десерт — обязателен к заказу."},
                "uz": {"name": "Dmitriy", "text": "Ajoyib vino tanlovi va oshpazning degustatsion menyusi — sinab ko'rishga arziydigan tajriba. Shirinlik uchun tiramisu — buyurtma qilish shart."},
            }},
            {"order": 5, "translations": {
                "en": {"name": "Sophie", "text": "Perfect spot for business lunches. Quick service, reasonable prices, and the Caesar salad is simply outstanding."},
                "ru": {"name": "Софи", "text": "Отличное место для бизнес-ланчей. Быстрое обслуживание, разумные цены, а салат Цезарь просто превосходен."},
                "uz": {"name": "Sofi", "text": "Biznes tushliklar uchun ajoyib joy. Tez xizmat ko'rsatish, maqul narxlar va Sezar salati shunchaki ajoyib."},
            }},
            {"order": 6, "translations": {
                "en": {"name": "Tom", "text": "The Sunday brunch is incredible value for money. So many choices, everything fresh, and the kids love the dessert station."},
                "ru": {"name": "Том", "text": "Воскресный бранч — невероятное соотношение цены и качества. Большой выбор, всё свежее, а дети обожают десертную станцию."},
                "uz": {"name": "Tom", "text": "Yakshanba brunchi — narx va sifatning ajoyib nisbati. Ko'p tanlov, hammasi yangi, bolalar esa shirinlik stansiyasini yaxshi ko'radilar."},
            }},
        ]
        for t in testimonials:
            name_en = t["translations"]["en"]["name"]
            text_en = t["translations"]["en"]["text"]
            Testimonial.objects.create(name=name_en, text=text_en, order=t["order"], translations=t["translations"])
        self.stdout.write(f"  Created {len(testimonials)} testimonials")

    def _create_about(self):
        if AboutContent.objects.exists():
            self.stdout.write("  About exists, skipping")
            return
        AboutContent.objects.create(
            title="Welcome to London Grill",
            content="London Grill is not just a restaurant. It is a place where English culinary traditions meet modern gastronomic trends. Our chef with 15 years of experience personally selects products at local markets so that every dish is fresh and unique.",
            translations={
                "ru": {
                    "title": "Добро пожаловать в London Grill",
                    "content": "London Grill — это не просто ресторан. Это место, где встречаются традиции английской кухни и современные гастрономические тенденции. Наш шеф-повар с 15-летним опытом лично отбирает продукты на локальных рынках, чтобы каждое блюдо было свежим и неповторимым.\n\nМы гордимся уютной атмосферой, внимательным сервисом и, конечно, нашей открытой кухней — вы всегда видите, как рождаются ваши любимые блюда.\n\nИнтерьер ресторана сочетает классический британский стиль с современными акцентами. У нас есть уютный зал на 50 мест, летняя терраса и отдельный VIP-зал для частных мероприятий.\n\nЖдём вас каждый день с 08:00 до 00:00. Бронирование столов по телефону +1 212-344-1230."
                },
                "en": {
                    "title": "Welcome to London Grill",
                    "content": "London Grill is not just a restaurant. It is a place where English culinary traditions meet modern gastronomic trends. Our chef with 15 years of experience personally selects products at local markets so that every dish is fresh and unique.\n\nWe are proud of our cozy atmosphere, attentive service and, of course, our open kitchen — you can always see how your favorite dishes are created.\n\nThe restaurant interior combines classic British style with modern accents. We have a cozy hall for 50 guests, a summer terrace, and a separate VIP room for private events.\n\nWe look forward to seeing you every day from 08:00 to 00:00. Table reservations: +1 212-344-1230."
                },
                "uz": {
                    "title": "London Grillga xush kelibsiz",
                    "content": "London Grill shunchaki restoran emas. Bu ingliz oshpazlik an'analari zamonaviy gastronomik tendentsiyalar bilan uchrashadigan joy. 15 yillik tajribaga ega oshpazimiz har bir taom yangi va noyob bo'lishi uchun mahalliy bozorlardan mahsulotlarni shaxsan tanlaydi.\n\nBiz qulay atmosferamiz, e'tiborli xizmatimiz va, albatta, ochiq oshxonamiz bilan faxrlanamiz — siz sevimli taomlaringiz qanday yaratilishini doim ko'rishingiz mumkin.\n\nRestoran interyeri klassik Britaniya uslubini zamonaviy aksentlar bilan uyg'unlashtiradi. Bizda 50 kishilik qulay zal, yozgi terassa va shaxsiy tadbirlar uchun alohida VIP xona mavjud.\n\nHar kuni soat 08:00 dan 00:00 gacha kutib qolamiz. Stol bron qilish: +1 212-344-1230."
                },
            }
        )
        self.stdout.write("  Created about page")

    def _create_contacts(self):
        if ContactMessage.objects.exists():
            self.stdout.write("  Contacts exist, skipping")
            return
        msgs = [
            {"name": "Анна", "email": "anna@example.com", "message": "Добрый день! Хотим забронировать столик на 25 декабря на 4 человека.", "is_read": True},
            {"name": "Марат", "email": "marat@example.com", "message": "Подскажите, есть ли у вас вегетарианское меню?", "is_read": True},
            {"name": "Елена", "email": "elena@example.com", "message": "Очень понравился ваш ресторан! Особенно десерты. Обязательно придём ещё!", "is_read": False},
        ]
        for m in msgs:
            ContactMessage.objects.create(**m)
        self.stdout.write(f"  Created {len(msgs)} contact messages")

    def _download_images(self):
        self.stdout.write("  Downloading images...")
        try:
            call_command('download_images')
        except Exception as e:
            self.stdout.write(f"  Skipped: {e}")
