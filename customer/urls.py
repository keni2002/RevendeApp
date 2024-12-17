from django.urls import path
from . import views
app_name = 'customer'
urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('detail/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('edit/<int:pk>/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    path('delete/<int:pk>/', views.CustomerDeleteView.as_view(), name='customer_delete'),
]
