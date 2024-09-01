from django.db import models


class Token(models.Model):
    unique_hash = models.CharField(unique=True, verbose_name="Уникальный хеш", blank=True, max_length=20)
    tx_hash = models.CharField(
        unique=True,
        verbose_name="Хэш транзакции создания токена",
        blank=True,
        max_length=100,
    )
    media_url = models.CharField(verbose_name="Картинка", max_length=100)
    owner = models.CharField(verbose_name="адрес пользователя в сети Ethereum", max_length=100)
