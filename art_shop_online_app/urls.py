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
    path('profile/<int:prof_id>', views.profile, name='profile'),
    path('profile/<int:prof_id>/edit', views.edit_profile, name='edit_profile'),
    path('products/', views.products_set, name='products_set'),
    path('checkout/', views.start_checkout, name='start_checkout'),
    path('products/json/', views.products_set_json, name='products_set_json'),
    path('products/<int:product_id>', views.product_view, name='product_details'),
    path('products/<int:product_id>/add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('products/<int:product_id>/remove-from-cart', views.remove_from_cart, name='remove_from_cart'),
    path ('products/<int:product_id>/comment', views.send_comment, name='send_comment'),
    path("payment/<int:order_id>/", views.fake_payment, name="fake_payment"),
    path("payment/<int:order_id>/success", views.payment_success, name="payment_success"),
    path("payment/<int:order_id>/cancel", views.payment_cancel, name="payment_cancel"),
    path("receipts/<int:receipt_id>/download/", views.download_receipt_xml, name="download-receipt-xml")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
