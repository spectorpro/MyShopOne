from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Поля, которые видны в списке товаров
    list_display = ('id', 'name', 'price', 'category', 'created_at')

    # Фильтры справа
    list_filter = ('category', 'created_at')

    # Поиск по названию и описанию
    search_fields = ('name', 'description', 'category__name')

    # Поля, доступные для редактирования на странице товара
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image')
        }),
        ('Цена и категория', {
            'fields': ('price', 'category')
        }),
    )

    list_per_page = 20
