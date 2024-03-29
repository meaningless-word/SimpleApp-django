from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Product, Category, Subscription
from .filters import ProductFilter

class ProductsListView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том, как именно пользователю будут показаны объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты. его нужно указывать, чтоб обратиться к списку объектов в html-шаблоне
    context_object_name = 'products'
    # Указывает количество записей на странице
    paginate_by = 3

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # получаем обычный запрос
        queryset = super().get_queryset()
        # используем наш класс фильтрации
        # self.request.GET содержит объект QueryDict, который мы рассматривали ране
        # сохраняем нашу фильтрацию в объекте класса, чтобы потом добавить в контекст
        # и использовать в шаблоне
        self.filterset = ProductFilter(self.request.GET, queryset)
        # возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    # Метод get_context_data позволяет нам изменить набор данных, который будет передан в шаблон
    def get_context_data(self, **kwargs):
        # с помощью super() мы обращаемся к родительским классам и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам. В ответе мы должны получить словарь
        context = super().get_context_data(**kwargs)
        # к словарю добавим текущую дату в ключ 'time_now'
        context['time_now'] = datetime.utcnow()
        # добавим ещё одну пустую переменную, чтобы на её примере рассмотреть работу ещё одного фильтра
        context['next_sale'] = None
        # добавляем в контекст объект фильтрации
        context['filterset'] = self.filterset
        return context


class ProductDetailView(DetailView):
    # Модель та же, но отображает отдельный товар
    model = Product
    # Используем другой шаблон
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'


# представление для создания товаров в функциональном стиле
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/products/')

    return render(request, 'product_edit.html', {'form': form})


# Добавляем новое представление для создания товаров посредством классов
class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    # указываем разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма
    template_name = 'product_edit.html'


# Добавляем представление для изменения товара.
class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_product',)
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(user=request.user, category=category,).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(user=request.user, category=OuterRef('pk'),)
        )
    ).order_by('name')

    return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions},)


