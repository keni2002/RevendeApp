from django.urls import path
from . import  views

app_name = 'sales'

urlpatterns = [
    path('', views.sale_list, name='sale_list'),
    # path('<int:pk>/', SaleDetailView.as_view(), name='sale_detail'),
    path('create/', views.sale_create, name='sale_create'),
    path('edit/<int:pk>/', views.sale_edit, name='sale_edit'),
    path('delete/<int:pk>/', views.sale_delete, name='sale_delete'),
]
