from django.db import models


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'news article'
        verbose_name_plural = 'news articles'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
