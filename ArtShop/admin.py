from django.contrib import admin
from .models import Product, Account, Receipt, ReceiptProduct

# Register your models here.

admin.site.register(Product)
admin.site.register(Account)
admin.site.register(Receipt)
admin.site.register(ReceiptProduct)
