from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создаёт группу “Модератор продуктов” и назначает права'

    def handle(self, *args, **options):
        group_name = 'Модератор продуктов'
        group, _ = Group.objects.get_or_create(name=group_name)

        content_type = ContentType.objects.get_for_model(Product)

        perm, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=content_type
        )
        group.permissions.add(perm)

        delete_perm = Permission.objects.filter(
            content_type=content_type,
            codename='delete_product'
        ).first()
        if delete_perm:
            group.permissions.add(delete_perm)

        self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" и права созданы.'))
