from django.urls import path
from .views import ProductsListView, ProductDetailView

urlpatterns = [
    path('', ProductsListView.as_view()),
    path('<int:pk>/', ProductDetailView.as_view()),
]