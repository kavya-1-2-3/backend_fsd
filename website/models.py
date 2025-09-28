from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class AuthUser(AbstractUser):
    # Custom user model
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    # Removing default fields if you don’t need them
    first_name = None
    last_name = None
    groups = None
    user_permissions = None

    def __str__(self):
        return self.email


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name


# class Review(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
#     user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='reviews')  # ✅ Added
#     rating = models.IntegerField()
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.email} - {self.product.name} ({self.rating} stars)"
from django.conf import settings

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} for {self.product.name} - {self.rating} stars"



# ✅ Correct signal for auth token creation
@receiver(post_save, sender=AuthUser)
def create_auth_user_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)