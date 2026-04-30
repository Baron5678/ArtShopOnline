from django.contrib.auth.models import User
from django.db import models

class ArtProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to='uploads', width_field='image_width', height_field='image_height')
    image_width = models.IntegerField(editable=True, null=True)
    image_height = models.IntegerField(editable=True, null=True)
    paint_type = models.CharField(max_length=30)
    material = models.CharField(max_length=30)
    genre = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    copies = models.PositiveIntegerField(default=1)
    rate = models.PositiveBigIntegerField(default=0, db_default=0)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    cart = models.ManyToManyField(ArtProduct, blank=True, related_name="profiles")
    avatar_width = models.IntegerField(editable=False, null=True)
    avatar_height = models.IntegerField(editable=False, null=True)
    avatar = models.ImageField(upload_to='uploads', width_field='avatar_width', height_field='avatar_height')


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(ArtProduct, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(ArtProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveBigIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "product"],
                name="unique_product_per_profile_cart"
            )
        ]

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.profile.user.username} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(ArtProduct, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField()

    def total_price(self):
        return self.price * self.amount

    def __str__(self):
        return f"{self.product_name} x {self.amount}"

class Receipt(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receipts")
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="receipt")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default="Fake card")
    billing_address = models.TextField(blank=True)
    shipping_address = models.TextField(blank=True)
