from django.contrib.auth.models import User
from django.db import models

class ArtProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to='uploads', width_field='image_width', height_field='image_height')
    image_width = models.IntegerField(editable=False, null=True)
    image_height = models.IntegerField(editable=False, null=True)
    paint_type = models.CharField(max_length=30)
    material = models.CharField(max_length=30)
    genre = models.CharField(max_length=30)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    cart = models.ManyToManyField(ArtProduct, blank=True, related_name="profiles")
    avatar_width = models.IntegerField(editable=False, null=True)
    avatar_height = models.IntegerField(editable=False, null=True)
    avatar = models.ImageField(upload_to='uploads', width_field='avatar_width', height_field='avatar_height')

class Receipt(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receipts')
    total_price = models.PositiveBigIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    billing_address = models.TextField()
    shipping_address = models.TextField()
    products = models.ManyToManyField(ArtProduct, related_name='receipts')