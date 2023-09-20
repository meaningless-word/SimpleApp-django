from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        ## fields = '__all__' # не очень хороший путь - в таблицах бывают поля, которые непозволительно отдавать на редактирование пользователю
        fields = [
            'name',
            'description',
            'category',
            'price',
            'quantity',
        ]