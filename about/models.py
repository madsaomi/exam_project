from django.db import models


class AboutContent(models.Model):
    title = models.CharField(max_length=255, default='О нас')
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'about content'
        verbose_name_plural = 'about content'

    def __str__(self):
        return self.title
