from django.db import models


class Token(models.Model):
    unique_hash = models.CharField(
        unique=True,
        verbose_name='Уникальный хеш',
        blank=True
    )
    tx_hash = models.CharField(
        unique=True,
        verbose_name='Хэш транзакции создания токена',
        blank=True
    )
    media_url = models.CharField(
        verbose_name='Картинка',
    )
    owner = models.CharField(
        verbose_name='адрес пользователя в сети Ethereum'
    )
