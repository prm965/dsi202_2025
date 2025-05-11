from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('signin/', views.login_user, name='signin'),
    path('logout/', views.logout_user, name='logout'),
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('home/', views.home, name='home'),
    path('service-details/', views.service_details, name='service_details'),
    path('starter-page/', views.starter_page, name='starter_page'),
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/decrease/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),

]
