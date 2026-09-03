from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Очищает БД и загружает тестовые данные'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем очистку базы данных...')

        # 1. Удаляем все продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('База данных очищена.')

        # 2. Создаем тестовые данные
        self.stdout.write('Создаем тестовые категории...')
        cat_test = Category.objects.create(name='Тестовая категория', description='Для проверки команды')

        self.stdout.write('Создаем тестовые товары...')
        Product.objects.create(
            name='Тестовый товар 1',
            description='Описание тестового товара',
            category=cat_test,
            price=100.00
        )
        Product.objects.create(
            name='Тестовый товар 2',
            description='Еще один тестовый товар',
            category=cat_test,
            price=200.00
        )

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))
