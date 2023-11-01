from django.core.management.base import BaseCommand, CommandError
from app.models import Product


class Command(BaseCommand):
    help = 'Обнуляет количство всех товаров'

    def handle(self, *args, **options):
        for product in Product.objects.all():
            product.quantity = 0
            product.save()

            self.stdout.write(self.style.SUCCESS('Seccessfully nulled product "%s"' % str(product)))

