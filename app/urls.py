from django.urls import path
from .views import (
    ProductsListView, ProductDetailView, create_product, ProductCreate, ProductUpdate, ProductDelete,
    subscriptions
)

urlpatterns = [
    path('', ProductsListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', create_product, name='product_create'),
    path('createbygen/', ProductCreate.as_view(), name='product_create_by_generic'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
