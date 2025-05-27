from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('pay/', views.pay, name='pay'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),  # ตรวจสอบว่า URL นี้มีอยู่
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_menu, name='restaurant_menu'),
    path('select-delivery-fee/', views.select_delivery_fee, name='select_delivery_fee'),
    path('select-address/', views.select_address, name='select_address'),
    path('promotion/', views.promotion_page, name='promotion'),
    path('message/', views.message_page, name='message'),
    path('profile/', views.profile_view, name='profile'),
    path('review/', views.review_board, name='review'),
    path('logout/', views.logout_view, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('address/add/', views.add_address, name='add_address'),
    path('pay/', views.pay, name='pay'),
    path('home/', views.home, name='home'),
    path('address/', views.address_list, name='address'),
    path('service-details/', views.service_details, name='service_details'),
    path('starter-page/', views.starter_page, name='starter_page'),
    path('menu/<int:pk>/', views.menu_detail, name='menu_detail'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/decrease/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
