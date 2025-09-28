from django.contrib import admin

# Register your models here.
from website.models import Product
from website.models import Review
from website.models import AuthUser
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(AuthUser)