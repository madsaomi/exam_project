from django.db import models


class TranslationMixin:
    def _t(self, field, lang='ru'):
        try:
            return self.translations.get(lang, {}).get(field, getattr(self, field, ''))
        except:
            return getattr(self, field, '')


class Category(models.Model, TranslationMixin):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    translations = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('order', 'name')

    def __str__(self):
        return self.name


class Testimonial(models.Model, TranslationMixin):
    name = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)
    translations = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name


class Dish(models.Model, TranslationMixin):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='dishes'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    translations = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'dish'
        verbose_name_plural = 'dishes'
        ordering = ('order', 'name')
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name'],
                name='unique_dish_in_category'
            )
        ]

    def __str__(self):
        return self.name
