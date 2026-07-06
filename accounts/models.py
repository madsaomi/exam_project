from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Avatar')

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
