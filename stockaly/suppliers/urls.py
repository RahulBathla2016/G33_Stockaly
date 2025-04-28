from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_dashboard, name='supplier_dashboard'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.add_supplier, name='add_supplier'),
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('suppliers/<int:pk>/edit/', views.edit_supplier, name='edit_supplier'),
    path('suppliers/<int:pk>/delete/', views.delete_supplier, name='delete_supplier'),
    path('suppliers/<int:supplier_id>/add-product/', views.add_supplier_product, name='add_supplier_product'),
    path('products/<int:pk>/edit/', views.edit_supplier_product, name='edit_supplier_product'),
    path('products/<int:pk>/delete/', views.delete_supplier_product, name='delete_supplier_product'),
    path('purchase-orders/', views.purchase_order_list, name='purchase_order_list'),
    path('purchase-orders/add/', views.add_purchase_order, name='add_purchase_order'),
    path('purchase-orders/<int:pk>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('purchase-orders/<int:pk>/edit/', views.edit_purchase_order, name='edit_purchase_order'),
    path('purchase-orders/<int:pk>/delete/', views.delete_purchase_order, name='delete_purchase_order'),
    path('purchase-orders/<int:order_id>/add-item/', views.add_order_item, name='add_order_item'),
    path('export-suppliers/', views.export_suppliers_csv, name='export_suppliers_csv'),
]