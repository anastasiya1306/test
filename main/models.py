from django.db import models

from blog.models import Blog
from users.models import User, NULLABLE


class Subscription(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='Контент')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    status = models.BooleanField(default=False, verbose_name='Статус подписки')
    payment_status = models.BooleanField(default=False, verbose_name='Статус оплаты')
    payment_date = models.DateField(**NULLABLE, verbose_name='Дата оплаты')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} - {self.blog}'
