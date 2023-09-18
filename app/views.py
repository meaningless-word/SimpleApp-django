from django.views.generic import ListView, DetailView
from .models import Product
from datetime import datetime


class ProductsListView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том, как именно пользователю будут показаны объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты. его нужно указывать, чтоб обратиться к списку объектов в html-шаблоне
    context_object_name = 'products'

    # Метод get_context_data позволяет нам изменить набор данных, который будет передан в шаблон
    def get_context_data(self, **kwargs):
        # с помощью super() мы обращаемся к родительским классам и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам. В ответе мы должны получить словарь
        context = super().get_context_data(**kwargs)
        # к словарю добавим текущую дату в ключ 'time_now'
        context['time_now'] = datetime.utcnow()
        # добавим ещё одну пустую переменную, чтобы на её примере рассмотреть работу ещё одного фильтра
        context['next_sale'] = None
        return context

class ProductDetailView(DetailView):
    # Модель та же, но отображает отдельный товар
    model = Product
    # Используем другой шаблон
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'

