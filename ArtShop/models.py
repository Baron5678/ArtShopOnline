from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to='uploads', width_field='image_width', height_field='image_height')
    image_width = models.IntegerField(editable=False, null=True)
    image_height = models.IntegerField(editable=False, null=True)
    paint_type = models.CharField(max_length=30)
    material = models.CharField(max_length=30)
    genre = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    desired_products = models.ManyToManyField(Product, blank=True, related_name="accounts")
    avatar_width = models.IntegerField(editable=False, null=True)
    avatar_height = models.IntegerField(editable=False, null=True)
    avatar = models.ImageField(upload_to='uploads', width_field='avatar_width', height_field='avatar_height')


class Cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='carts')
    products = models.ManyToManyField(Product, through='CartProduct', related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart of {self.account.user.username}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart"


class Receipt(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receipts')
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True, related_name='receipts')
    total_price = models.PositiveBigIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)  # e.g., 'Credit Card', 'PayPal', 'Cash'
    billing_address = models.TextField()
    shipping_address = models.TextField()
    products = models.ManyToManyField(Product, through='ReceiptProduct', related_name='receipts')

    def __str__(self):
        return f"Receipt #{self.id} for {self.account.user.username}"


class ReceiptProduct(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.PositiveBigIntegerField()  # Price of the product at the time of purchase

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Receipt #{self.receipt.id}"
