from django.db import models


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    translations = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'news article'
        verbose_name_plural = 'news articles'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def _t(self, field, lang='ru'):
        try:
            return self.translations.get(lang, {}).get(field, getattr(self, field, ''))
        except:
            return getattr(self, field, '')
