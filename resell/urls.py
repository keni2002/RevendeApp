from django.urls import path
from . import views
app_name = 'resell'
urlpatterns = [
    path('',views.product_list,name='products'),
    path('tags/<slug:categories_slug>/',views.product_list,name='product_list_by_category'),
    path('add/', views.ProductCreateView.as_view(), name='product_add'),
    # path('delete/<pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('edit/<pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('detail/<pk>', views.ProductDetailView.as_view(), name='product_detail'),
]


