import os
import django
import urllib.request
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from menu.models import Dish

images = [
    'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&h=380&fit=crop', # Salad
    'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&h=380&fit=crop', # Pizza
    'https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=500&h=380&fit=crop', # Burger
    'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=500&h=380&fit=crop', # Pasta
    'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=500&h=380&fit=crop', # Steak
    'https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?w=500&h=380&fit=crop', # Dishes
    'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&h=380&fit=crop', # BBQ
    'https://images.unsplash.com/photo-1600891964092-4316c288032e?w=500&h=380&fit=crop', # Steak
    'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=500&h=380&fit=crop', # Fish
    'https://images.unsplash.com/photo-1555985202-12975b0235dc?w=500&h=380&fit=crop', # Pasta
    'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=500&h=380&fit=crop', # Salad
    'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=500&h=380&fit=crop'  # Dessert
]

dishes = Dish.objects.all()

for i, dish in enumerate(dishes):
    url = images[i % len(images)]
    print(f"Downloading image for {dish.name}...")
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    img_temp = NamedTemporaryFile(delete=True)
    try:
        with urllib.request.urlopen(req) as response:
            img_temp.write(response.read())
        img_temp.flush()
        
        dish.image.save(f"dish_{dish.id}.jpg", File(img_temp), save=True)
        print(f"Saved {dish.name}")
    except Exception as e:
        print(f"Failed for {dish.name}: {e}")

print("Done downloading images.")
