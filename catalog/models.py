from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование категории'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание категории'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        # Опционально: сортировка по умолчанию
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование товара'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание товара'
    )
    # upload_to='products/' создаст папку products внутри MEDIA_ROOT
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Изображение товара'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at'] # По умолчанию сортируем новые товары первыми

    def __str__(self):
        return f"{self.name} ({self.category.name})"
