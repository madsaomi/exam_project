from django.db import models


class AboutContent(models.Model):
    title = models.CharField(max_length=255, default='About Us')
    content = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    translations = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = 'about content'
        verbose_name_plural = 'about contents'

    def __str__(self):
        return self.title

    def _t(self, field, lang='ru'):
        try:
            return self.translations.get(lang, {}).get(field, getattr(self, field, ''))
        except:
            return getattr(self, field, '')
