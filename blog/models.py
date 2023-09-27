from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit
import uuid
from users.models import NULLABLE, User


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.SlugField(max_length=150, verbose_name='URL', unique=True)
    description = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blogs/', verbose_name='Изображение', **NULLABLE)
    date_creation = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    is_publication = models.BooleanField(default=True, verbose_name='Признак публикации')
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', **NULLABLE)
    payment_amount = models.IntegerField(default=0, verbose_name='Стоимость подписки')
    is_paid = models.BooleanField(default=False, verbose_name='Контент платный')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Преобразование заголовка в slug"""
        if not self.slug:
            # Транслитерация заголовка статьи с русского на английский
            title_translate = translit(self.title, 'ru', reversed=True)
            self.slug = slugify(title_translate, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
