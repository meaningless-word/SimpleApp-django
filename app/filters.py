from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from .models import Product, Category, Material


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class ProductFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='category', # имя поля в Product, для которого создаётся выпадающий список
        queryset=Category.objects.all(), # в список попадут все категории
        label='Категория', # метка для обозначения списка
        empty_label='любой', # замена строчки --------- в начале списка, обозначающего отсутствие фильтра на вменяемое название
    )
    material = ModelMultipleChoiceFilter(
        field_name='productmaterial__material',
        queryset=Material.objects.all(),
        label='Материал',
        conjoined=True, # значение True ставится для того, чтобы фильтр работал с условием and, т.е. все выбранные материалы должны быть в каждом из фильтруемых продуктов
                        # хотя по-умолчанию стоит False, что означает что были бы выбраны все продукты, содержищие хотя бы один из выбранных материалов в списке
    )
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Product
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'name': ['icontains'],
            # количество товаров должно быть больше или равно
            'quantity': ['gt'],
            'price': [
                'lt',  # цена должна быть меньше или равна указанной
                'gt',  # цена должна быть больше или равна указанной
            ],
            #'category': ['exact'],
            #'productmaterial__material': ['exact'],
        }
