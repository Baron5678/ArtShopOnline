# myapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profile/<int:acc_id>', views.account, name='account'),
    path('profile/<int:acc_id>/edit', views.edit_account, name='edit_account'),
    path('profile/<int:acc_id>/cart', views.cart_view, name='cart_view'),
    path('products/', views.products_set, name='products_set'),
    path('products/json/', views.products_set_json, name='products_set_json'),
    path('products/<int:product_id>', views.product_view, name='product_details'),
    path('products/<int:product_id>/add-to-cart', views.add_to_cart, name='add_to_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
