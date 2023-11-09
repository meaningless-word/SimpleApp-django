from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()


class Material(models.Model):
    # наименование материала
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()


# Товар для нашей витрины
class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)  # названия товаров не должны повторяться
    description = models.TextField()
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='products')  # все продукты в категории будут доступны через поле products
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    materials = models.ManyToManyField(Material, through='ProductMaterial')

    # допишем свойство, которое будет отображать есть ли товар на складе
    @property
    def on_stock(self):
        return self.quantity > 0

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])  # Указывает куда редиректиться после додбавления новой записи

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} | {self.material.name}'


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions',)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='subscriptions',)
