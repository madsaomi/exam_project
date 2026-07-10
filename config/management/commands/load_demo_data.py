from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from menu.models import Category, Dish, Testimonial
from news.models import NewsArticle
from about.models import AboutContent

User = get_user_model()


class Command(BaseCommand):
    help = 'Load demo data: categories, dishes, news, about, testimonials'

    def handle(self, *args, **options):
        self._load_categories()
        self._load_dishes()
        self._load_news()
        self._load_about()
        self._load_testimonials()
        self.stdout.write(self.style.SUCCESS('Demo data loaded successfully'))

    def _load_categories(self):
        if Category.objects.exists():
            self.stdout.write('Categories already exist, skipping')
            return
        cats = [
            {
                'name': 'Appetizers',
                'translations': {
                    'ru': {'name': 'Закуски', 'description': 'Лёгкие и вкусные закуски для начала трапезы'},
                    'uz': {'name': 'Aperitivlar', 'description': 'Engil va mazali gazaklar'},
                    'en': {'name': 'Appetizers', 'description': 'Light and tasty starters to begin your meal'},
                },
                'order': 1,
            },
            {
                'name': 'Main Courses',
                'translations': {
                    'ru': {'name': 'Основные блюда', 'description': 'Сытные блюда из мяса, рыбы и птицы'},
                    'uz': {'name': 'Asosiy taomlar', 'description': 'Go\'sht, baliq va parranda go\'shtidan tayyorlangan to\'yimli taomlar'},
                    'en': {'name': 'Main Courses', 'description': 'Hearty meat, fish and poultry dishes'},
                },
                'order': 2,
            },
            {
                'name': 'Grill Specials',
                'translations': {
                    'ru': {'name': 'Гриль', 'description': 'Сочные стейки и барбекю на открытом огне'},
                    'uz': {'name': 'Gril', 'description': 'Ochiq olovda pishirilgan suvli bifteklar va barbekyu'},
                    'en': {'name': 'Grill Specials', 'description': 'Juicy steaks and barbecue cooked over an open flame'},
                },
                'order': 3,
            },
            {
                'name': 'Salads',
                'translations': {
                    'ru': {'name': 'Салаты', 'description': 'Свежие салаты из сезонных овощей'},
                    'uz': {'name': 'Salatlar', 'description': 'Mavsumiy sabzavotlardan tayyorlangan yangi salatlar'},
                    'en': {'name': 'Salads', 'description': 'Fresh salads made with seasonal vegetables'},
                },
                'order': 4,
            },
            {
                'name': 'Desserts',
                'translations': {
                    'ru': {'name': 'Десерты', 'description': 'Нежные и сладкие угощения на любой вкус'},
                    'uz': {'name': 'Shirinliklar', 'description': 'Har qanday ta\'mga mos nozik va shirinliklar'},
                    'en': {'name': 'Desserts', 'description': 'Delightful sweet treats for every taste'},
                },
                'order': 5,
            },
            {
                'name': 'Drinks',
                'translations': {
                    'ru': {'name': 'Напитки', 'description': 'Освежающие напитки, соки и коктейли'},
                    'uz': {'name': 'Ichimliklar', 'description': 'Tetiklantiruvchi ichimliklar, sharbatlar va kokteyllar'},
                    'en': {'name': 'Drinks', 'description': 'Refreshing beverages, juices and cocktails'},
                },
                'order': 6,
            },
        ]
        for data in cats:
            t = data.pop('translations')
            cat = Category.objects.create(**data)
            cat.translations = t
            cat.save(update_fields=['translations'])

    def _load_dishes(self):
        if Dish.objects.exists():
            self.stdout.write('Dishes already exist, skipping')
            return
        cat_map = {c.name: c for c in Category.objects.all()}
        dishes = [
            {
                'category': cat_map['Appetizers'],
                'name': 'Bruschetta',
                'price': 8.50,
                'order': 1,
                'translations': {
                    'ru': {'name': 'Брускетта', 'description': 'Тосты с помидорами, базиликом и оливковым маслом'},
                    'uz': {'name': 'Brusshetta', 'description': 'Pomidor, rayhon va zaytun moyi bilan tostlar'},
                    'en': {'name': 'Bruschetta', 'description': 'Toasted bread with tomatoes, basil and olive oil'},
                },
            },
            {
                'category': cat_map['Appetizers'],
                'name': 'Garlic Shrimp',
                'price': 12.00,
                'order': 2,
                'translations': {
                    'ru': {'name': 'Креветки с чесноком', 'description': 'Тигровые креветки с чесноком и лимоном'},
                    'uz': {'name': 'Sarimsoqli qisqichbaqalar', 'description': 'Sarimsoq va limon bilan yo\'lbaris qisqichbaqalari'},
                    'en': {'name': 'Garlic Shrimp', 'description': 'Tiger shrimp with garlic and lemon'},
                },
            },
            {
                'category': cat_map['Main Courses'],
                'name': 'Grilled Salmon',
                'price': 22.00,
                'order': 1,
                'translations': {
                    'ru': {'name': 'Лосось на гриле', 'description': 'Филе лосося с овощами и сливочным соусом'},
                    'uz': {'name': 'Grilda losos', 'description': 'Sabzavotlar va qaymoqli sous bilan losos filesi'},
                    'en': {'name': 'Grilled Salmon', 'description': 'Salmon fillet with vegetables and cream sauce'},
                },
            },
            {
                'category': cat_map['Main Courses'],
                'name': 'Beef Wellington',
                'price': 32.00,
                'order': 2,
                'translations': {
                    'ru': {'name': 'Говядина Веллингтон', 'description': 'Говяжья вырезка в слоёном тесте с грибным соусом'},
                    'uz': {'name': 'Vellington mol go\'shti', 'description': 'Qatlamali xamirda mol go\'shti, qo\'ziqorin sousi bilan'},
                    'en': {'name': 'Beef Wellington', 'description': 'Beef tenderloin wrapped in puff pastry with mushroom sauce'},
                },
            },
            {
                'category': cat_map['Grill Specials'],
                'name': 'Ribeye Steak',
                'price': 28.00,
                'order': 1,
                'translations': {
                    'ru': {'name': 'Стейк Рибай', 'description': 'Мраморная говядина на кости, подаётся с картофелем'},
                    'uz': {'name': 'Ribeye biftek', 'description': 'Suyakdagi marmar mol go\'shti, kartoshka bilan'},
                    'en': {'name': 'Ribeye Steak', 'description': 'Marbled bone-in beef served with potatoes'},
                },
            },
            {
                'category': cat_map['Grill Specials'],
                'name': 'BBQ Ribs',
                'price': 25.00,
                'order': 2,
                'translations': {
                    'ru': {'name': 'Барбекю рёбра', 'description': 'Свиные рёбра в домашнем соусе барбекю'},
                    'uz': {'name': 'Barbekyu qovurg\'alar', 'description': 'Uy barbekyu sousida cho\'chqa qovurg\'alari'},
                    'en': {'name': 'BBQ Ribs', 'description': 'Pork ribs glazed with house-made BBQ sauce'},
                },
            },
            {
                'category': cat_map['Salads'],
                'name': 'Caesar Salad',
                'price': 11.00,
                'order': 1,
                'translations': {
                    'ru': {'name': 'Цезарь', 'description': 'Римский салат с курицей, пармезаном и гренками'},
                    'uz': {'name': 'Sezar', 'description': 'Tovuq, parmezan va krutonlar bilan Rim salati'},
                    'en': {'name': 'Caesar Salad', 'description': 'Classic Caesar with chicken, parmesan and croutons'},
                },
            },
            {
                'category': cat_map['Salads'],
                'name': 'Greek Salad',
                'price': 10.00,
                'order': 2,
                'translations': {
                    'ru': {'name': 'Греческий салат', 'description': 'Овощи с фетой, маслинами и оливковым маслом'},
                    'uz': {'name': 'Yunon salati', 'description': 'Feta, zaytun va zaytun moyi bilan sabzavotlar'},
                    'en': {'name': 'Greek Salad', 'description': 'Fresh vegetables with feta, olives and olive oil'},
                },
            },
            {
                'category': cat_map['Desserts'],
                'name': 'Tiramisu',
                'price': 9.00,
                'order': 1,
                'translations': {
                    'ru': {'name': 'Тирамису', 'description': 'Классический итальянский десерт с маскарпоне'},
                    'uz': {'name': 'Tiramisu', 'description': 'Maskarpone bilan klassik italyan shirinligi'},
                    'en': {'name': 'Tiramisu', 'description': 'Classic Italian dessert with mascarpone cheese'},
                },
            },
            {
                'category': cat_map['Desserts'],
                'name': 'Chocolate Lava Cake',
                'price': 10.00,
                'order': 2,
                'translations': {
                    'ru': {'name': 'Шоколадный фондан', 'description': 'Горячий шоколадный кекс с жидкой начинкой'},
                    'uz': {'name': 'Shokoladli lava kek', 'description': 'Suyuq to\'ldirilgan issiq shokoladli kek'},
                    'en': {'name': 'Chocolate Lava Cake', 'description': 'Warm chocolate cake with a molten centre'},
                },
            },
            {
                'category': cat_map['Drinks'],
                'name': 'Fresh Orange Juice',
                'price': 5.00,
                'order': 1,
                'translations': {
                    'ru': {'name': 'Свежевыжатый апельсиновый сок', 'description': 'Натуральный апельсиновый сок'},
                    'uz': {'name': 'Yangi siqilgan apelsin sharbati', 'description': 'Tabiiy apelsin sharbati'},
                    'en': {'name': 'Fresh Orange Juice', 'description': 'Natural freshly squeezed orange juice'},
                },
            },
            {
                'category': cat_map['Drinks'],
                'name': 'Mojito',
                'price': 7.00,
                'order': 2,
                'translations': {
                    'ru': {'name': 'Мохито', 'description': 'Освежающий коктейль с мятой и лаймом'},
                    'uz': {'name': 'Moxito', 'description': 'Yalpiz va laym bilan tetiklantiruvchi kokteyl'},
                    'en': {'name': 'Mojito', 'description': 'Refreshing cocktail with mint and lime'},
                },
            },
        ]
        for data in dishes:
            t = data.pop('translations')
            dish = Dish.objects.create(**data)
            dish.translations = t
            dish.save(update_fields=['translations'])

    def _load_news(self):
        if NewsArticle.objects.exists():
            self.stdout.write('News already exist, skipping')
            return
        articles = [
            {
                'title': 'New Summer Menu',
                'content': 'We are excited to announce our new summer menu featuring fresh seasonal ingredients and creative dishes crafted by our head chef.',
                'translations': {
                    'ru': {'title': 'Новое летнее меню', 'content': 'С радостью представляем новое летнее меню со свежими сезонными ингредиентами и авторскими блюдами от нашего шеф-повара.'},
                    'uz': {'title': 'Yangi yozgi menyu', 'content': 'Biz sizni yangi yozgi menyu bilan tanishtirishdan xursandmiz. Unda mavsumiy mahsulotlar va bosh oshpazimizning ijodiy taomlari mavjud.'},
                },
            },
            {
                'title': 'Live Jazz Every Friday',
                'content': 'Join us every Friday evening for live jazz music. Enjoy great food and the best live music in the city from 7 PM.',
                'translations': {
                    'ru': {'title': 'Живой джаз каждую пятницу', 'content': 'Приходите к нам каждую пятницу вечером на живую джазовую музыку. Наслаждайтесь отличной едой и лучшей живой музыкой в городе с 19:00.'},
                    'uz': {'title': 'Har juma jonli jazz', 'content': 'Har juma kuni kechqurun jonli jazz musiqasi uchun keling. Soat 19:00 dan boshlab ajoyib taomlar va eng yaxshi jonli musiqadan zavqlaning.'},
                },
            },
            {
                'title': 'Wine Tasting Event',
                'content': 'Join our sommelier for an exclusive wine tasting evening. Taste 8 premium wines paired with gourmet appetizers.',
                'translations': {
                    'ru': {'title': 'Дегустация вин', 'content': 'Присоединяйтесь к нашему сомелье на эксклюзивном вечере дегустации вин. Попробуйте 8 премиальных вин в сочетании с изысканными закусками.'},
                    'uz': {'title': 'Vino degustatsiyasi', 'content': 'Eksklyuziv vino kechasida somelyerimizga qo\'shiling. 8 ta premium vinolarni va nozik gazaklarni tatib ko\'ring.'},
                },
            },
        ]
        for data in articles:
            t = data.pop('translations')
            article = NewsArticle.objects.create(**data)
            article.translations = t
            article.save(update_fields=['translations'])

    def _load_about(self):
        if AboutContent.objects.exists():
            self.stdout.write('About content already exists, skipping')
            return
        about = AboutContent.objects.create(
            title='About London Grill',
            content='London Grill House is a premier dining destination in the heart of London, offering a unique blend of traditional British cuisine and international flavours. Our experienced chefs use only the freshest ingredients to create unforgettable dishes. We pride ourselves on exceptional service and a warm, inviting atmosphere.',
        )
        about.translations = {
            'ru': {
                'title': 'О нас',
                'content': 'London Grill House — престижный ресторан в самом центре Лондона, предлагающий уникальное сочетание традиционной британской кухни и интернациональных вкусов. Наши опытные шеф-повара используют только свежайшие ингредиенты для создания незабываемых блюд. Мы гордимся исключительным сервисом и тёплой, гостеприимной атмосферой.',
            },
            'uz': {
                'title': 'Biz haqimizda',
                'content': 'London Grill House — London markazidagi nufuzli restoran bo\'lib, an\'anaviy Britaniya oshxonasi va xalqaro ta\'mlarning noyob uyg\'unligini taklif etadi. Tajribali oshpazlarimiz unutilmas taomlar yaratish uchun eng yangi ingredientlardan foydalanadilar. Biz ajoyib xizmat va iliq, mehmondo\'st muhit bilan faxrlanamiz.',
            },
        }
        about.save(update_fields=['translations'])

    def _load_testimonials(self):
        if Testimonial.objects.exists():
            self.stdout.write('Testimonials already exist, skipping')
            return
        items = [
            {
                'name': 'Sarah Johnson',
                'text': 'Absolutely amazing food and ambiance! The grilled salmon was perfectly cooked. Highly recommend!',
                'order': 1,
                'translations': {
                    'ru': {'name': 'Сара Джонсон', 'text': 'Потрясающая еда и атмосфера! Лосось на гриле был приготовлен идеально. Очень рекомендую!'},
                    'uz': {'name': 'Sara Jonson', 'text': 'Ajoyib taom va muhit! Grilda pishirilgan losos mukammal tayyorlangan edi. Tavsiya qilaman!'},
                },
            },
            {
                'name': 'Michael Brown',
                'text': 'The beef Wellington is the best I have ever had. The staff was incredibly attentive. Five stars!',
                'order': 2,
                'translations': {
                    'ru': {'name': 'Майкл Браун', 'text': 'Говядина Веллингтон — лучшее, что я когда-либо пробовал. Персонал был невероятно внимательным. Пять звёзд!'},
                    'uz': {'name': 'Maykl Braun', 'text': 'Vellington mol go\'shti men tatib ko\'rgan eng yaxshisi. Xodimlar juda e\'tiborli edi. Besh yulduz!'},
                },
            },
            {
                'name': 'Emily Davis',
                'text': 'Perfect place for a romantic dinner. The tiramisu was divine! Will definitely come back.',
                'order': 3,
                'translations': {
                    'ru': {'name': 'Эмили Дэвис', 'text': 'Идеальное место для романтического ужина. Тирамису было божественным! Обязательно вернусь.'},
                    'uz': {'name': 'Emili Devis', 'text': 'Romatik kechki ovqat uchun ajoyib joy. Tiramisu juda zo\'r edi! Albatta qaytib kelaman.'},
                },
            },
            {
                'name': 'James Wilson',
                'text': 'Excellent Sunday roast! The Yorkshire puddings were spot on. A true taste of Britain.',
                'order': 4,
                'translations': {
                    'ru': {'name': 'Джеймс Уилсон', 'text': 'Отличное воскресное жаркое! Йоркширские пудинги были бесподобны. Настоящий вкус Британии.'},
                    'uz': {'name': 'Jeyms Uilson', 'text': 'Ajoyib yakshanba qovurilgan taomi! Yorkshire pudinglari ajoyib edi. Britaniyaning haqiqiy ta\'mi.'},
                },
            },
        ]
        for data in items:
            t = data.pop('translations')
            item = Testimonial.objects.create(**data)
            item.translations = t
            item.save(update_fields=['translations'])
