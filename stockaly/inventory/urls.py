from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('index/', views.index, name='index'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add/', views.add_item, name='add_item'),
    path('view/<int:id>/', views.view_item, name='view_item'),
    path('edit/<int:id>/', views.edit_item, name='edit_item'),
    path('delete/<int:id>/', views.delete_item, name='delete_item'),
    # path('adminview/<int:id>/', views.admin_view_item, name='admin_view_item'),
    path('adminedit/<int:id>/', views.admin_edit_item, name='admin_edit_item'),
    path('admindelete/<int:id>/', views.admin_delete_item, name='admin_delete_item'),
    path('export/', views.export_csv, name='export_csv'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
]