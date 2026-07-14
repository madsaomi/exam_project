# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from menu.models import Category, Dish, Testimonial
from news.models import NewsArticle
from about.models import AboutContent

print("Starting fix...")

# 1. Categories
cat_ru = {
    'Appetizers': {'name': 'Закуски', 'description': 'Лёгкие и вкусные закуски для начала трапезы'},
    'Main Courses': {'name': 'Основные блюда', 'description': 'Сытные блюда из мяса, рыбы и птицы'},
    'Grill Specials': {'name': 'Гриль', 'description': 'Сочные стейки и барбекю на открытом огне'},
    'Salads': {'name': 'Салаты', 'description': 'Свежие салаты из сезонных овощей'},
    'Desserts': {'name': 'Десерты', 'description': 'Нежные и сладкие угощения на любой вкус'},
    'Drinks': {'name': 'Напитки', 'description': 'Освежающие напитки, соки и коктейли'},
}
for c in Category.objects.all():
    if c.name in cat_ru:
        c.translations['ru'] = cat_ru[c.name]
        c.save(update_fields=['translations'])

# 2. Dishes
dish_ru = {
    'Bruschetta': {'name': 'Брускетта', 'description': 'Тосты с помидорами, базиликом и оливковым маслом'},
    'Garlic Shrimp': {'name': 'Креветки с чесноком', 'description': 'Тигровые креветки с чесноком и лимоном'},
    'Grilled Salmon': {'name': 'Лосось на гриле', 'description': 'Филе лосося с овощами и сливочным соусом'},
    'Beef Wellington': {'name': 'Говядина Веллингтон', 'description': 'Говяжья вырезка в слоёном тесте с грибным соусом'},
    'Ribeye Steak': {'name': 'Стейк Рибай', 'description': 'Мраморная говядина на кости, подаётся с картофелем'},
    'BBQ Ribs': {'name': 'Барбекю рёбра', 'description': 'Свиные рёбра в домашнем соусе барбекю'},
    'Caesar Salad': {'name': 'Цезарь', 'description': 'Римский салат с курицей, пармезаном и гренками'},
    'Greek Salad': {'name': 'Греческий салат', 'description': 'Овощи с фетой, маслинами и оливковым маслом'},
    'Tiramisu': {'name': 'Тирамису', 'description': 'Классический итальянский десерт с маскарпоне'},
    'Chocolate Lava Cake': {'name': 'Шоколадный фондан', 'description': 'Горячий шоколадный кекс с жидкой начинкой'},
    'Fresh Orange Juice': {'name': 'Свежевыжатый апельсиновый сок', 'description': 'Натуральный апельсиновый сок'},
    'Mojito': {'name': 'Мохито', 'description': 'Освежающий коктейль с мятой и лаймом'},
}
# Don't touch Qozon kabob and Pahlava (they were already manually set correctly in the previous step, though if we look at their English names they were Qozon kabob/Pahlava too, wait, they were modified directly)
# I will just match by `name` field, which I modified earlier for those two. The other 10 should match.
for d in Dish.objects.all():
    if d.name in dish_ru:
        d.translations['ru'] = dish_ru[d.name]
        d.save(update_fields=['translations'])

# 3. News
news_ru = {
    'New Summer Menu': {'title': 'Новое летнее меню', 'content': 'С радостью представляем новое летнее меню со свежими сезонными ингредиентами и авторскими блюдами от нашего шеф-повара.'},
    'Live Jazz Every Friday': {'title': 'Живой джаз каждую пятницу', 'content': 'Приходите к нам каждую пятницу вечером на живую джазовую музыку. Наслаждайтесь отличной едой и лучшей живой музыкой в городе с 19:00.'},
    'Wine Tasting Event': {'title': 'Дегустация вин', 'content': 'Присоединяйтесь к нашему сомелье на эксклюзивном вечере дегустации вин. Попробуйте 8 премиальных вин в сочетании с изысканными закусками.'},
}
for n in NewsArticle.objects.all():
    if n.title in news_ru:
        n.translations['ru'] = news_ru[n.title]
        n.save(update_fields=['translations'])

# 4. About
about = AboutContent.objects.first()
if about:
    about.translations['ru'] = {
        'title': 'О нас',
        'content': 'London Grill House — престижный ресторан в самом центре Лондона, предлагающий уникальное сочетание традиционной британской кухни и интернациональных вкусов. Наши опытные шеф-повара используют только свежайшие ингредиенты для создания незабываемых блюд. Мы гордимся исключительным сервисом и тёплой, гостеприимной атмосферой.',
    }
    about.save(update_fields=['translations'])

# 5. Testimonials
test_ru = {
    'Sarah Johnson': {'name': 'Сара Джонсон', 'text': 'Потрясающая еда и атмосфера! Лосось на гриле был приготовлен идеально. Очень рекомендую!'},
    'Michael Brown': {'name': 'Майкл Браун', 'text': 'Говядина Веллингтон — лучшее, что я когда-либо пробовал. Персонал был невероятно внимательным. Пять звёзд!'},
    'Emily Davis': {'name': 'Эмили Дэвис', 'text': 'Идеальное место для романтического ужина. Тирамису было божественным! Обязательно вернусь.'},
    'James Wilson': {'name': 'Джеймс Уилсон', 'text': 'Отличное воскресное жаркое! Йоркширские пудинги были бесподобны. Настоящий вкус Британии.'},
}
for t in Testimonial.objects.all():
    if t.name in test_ru:
        t.translations['ru'] = test_ru[t.name]
        t.save(update_fields=['translations'])

print("Fix completed.")
