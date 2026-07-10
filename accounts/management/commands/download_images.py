import urllib.request
import urllib.parse
import os
import io
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.conf import settings
from menu.models import Dish, Category
from news.models import NewsArticle
from about.models import AboutContent


def download_image(url):
    try:
        r = urllib.request.urlopen(url, timeout=15)
        data = r.read()
        if len(data) < 1000:
            return None, f"too small ({len(data)} bytes)"
        return ContentFile(data), None
    except Exception as e:
        return None, str(e)


class Command(BaseCommand):
    help = "Downloads real food images from picsum.photos"

    def handle(self, *args, **options):
        self._dishes()
        self._news()
        self._about()
        self._categories()
        self.stdout.write(self.style.SUCCESS("Done!"))

    def _categories(self):
        cats = Category.objects.all()
        ok = 0
        for cat in cats:
            if cat.image:
                ok += 1
                continue
            seed = urllib.parse.quote(cat.name.lower().replace(' ', '-')[:30])
            url = f"https://picsum.photos/seed/cat-{seed}/500/380"
            img, err = download_image(url)
            if img:
                cat.image.save(f"cat_{cat.pk}.jpg", img, save=True)
                self.stdout.write(f"  OK {cat.name}")
                ok += 1
            else:
                self.stdout.write(f"  FAIL {cat.name}: {err}")
        self.stdout.write(f"  Categories: {ok}/{cats.count()}")

    def _dishes(self):
        dishes = Dish.objects.all()
        ok = 0
        for dish in dishes:
            if dish.image:
                ok += 1
                continue
            seed = urllib.parse.quote(dish.name.lower().replace(' ', '-')[:40])
            url = f"https://picsum.photos/seed/{seed}/500/380"
            img, err = download_image(url)
            if img:
                dish.image.save(f"dish_{dish.pk}.jpg", img, save=True)
                self.stdout.write(f"  OK {dish.name}")
                ok += 1
            else:
                self.stdout.write(f"  FAIL {dish.name}: {err}")
        self.stdout.write(f"  Dishes: {ok}/{dishes.count()}")

    def _news(self):
        articles = NewsArticle.objects.all()
        ok = 0
        for a in articles:
            if a.image:
                ok += 1
                continue
            seed = urllib.parse.quote(a.title.lower().replace(' ', '-')[:30])
            url = f"https://picsum.photos/seed/{seed}/800/500"
            img, err = download_image(url)
            if img:
                a.image.save(f"news_{a.pk}.jpg", img, save=True)
                self.stdout.write(f"  OK {a.title[:30]}")
                ok += 1
            else:
                self.stdout.write(f"  FAIL {a.title[:30]}: {err}")
        self.stdout.write(f"  News: {ok}/{articles.count()}")

    def _about(self):
        about = AboutContent.objects.first()
        if not about:
            return
        if about.image:
            self.stdout.write("  About: already has image")
            return
        url = "https://picsum.photos/seed/london-about/900/600"
        img, err = download_image(url)
        if img:
            about.image.save("about.jpg", img, save=True)
            self.stdout.write("  OK About image")
        else:
            self.stdout.write(f"  FAIL About: {err}")
