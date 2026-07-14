import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from menu.models import Dish

# Revert Qozon kabob -> BBQ Ribs
try:
    d = Dish.objects.get(name='Qozon kabob')
    d.name = 'BBQ Ribs'
    d.description = 'Tender pork ribs coated in our house-made BBQ sauce, served with fries.'
    if 'uz' in d.translations:
        d.translations['uz']['name'] = "Barbekyu qovurg'alar"
        d.translations['uz']['description'] = 'Uy qurilishi barbekyu sousidagi cho\'chqa qovurg\'alari, fri kartoshkasi bilan beriladi.'
    if 'ru' in d.translations:
        d.translations['ru']['name'] = 'Барбекю рёбра'
        d.translations['ru']['description'] = 'Свиные рёбра в домашнем соусе барбекю'
    d.save()
    print("Reverted Qozon kabob to BBQ Ribs.")
except Dish.DoesNotExist:
    pass

# Revert Pahlava -> Chocolate Lava Cake
try:
    d = Dish.objects.get(name='Pahlava')
    d.name = 'Chocolate Lava Cake'
    d.description = 'Warm chocolate cake with a molten center, served with vanilla ice cream.'
    if 'uz' in d.translations:
        d.translations['uz']['name'] = 'Shokoladli lava kek'
        d.translations['uz']['description'] = 'Issiq shokoladli tort erigan markaz bilan, vanil muzqaymoq bilan tortiq etiladi.'
    if 'ru' in d.translations:
        d.translations['ru']['name'] = 'Шоколадный фондан'
        d.translations['ru']['description'] = 'Горячий шоколадный кекс с жидкой начинкой'
    d.save()
    print("Reverted Pahlava to Chocolate Lava Cake.")
except Dish.DoesNotExist:
    pass
