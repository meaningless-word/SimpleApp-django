from django.urls import path
from .views import ProductsListView, ProductDetailView, create_product

urlpatterns = [
    path('', ProductsListView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
    path('create/', create_product, name='product_create'),
]
