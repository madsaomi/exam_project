from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('order', 'name')

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='dishes'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
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
