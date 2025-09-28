# website/api/urls.py - FINAL CODE

from django.urls import path
from . import views  # <-- This correctly imports your custom API views (product_list, etc.)
from rest_framework.authtoken import views as drf_views # <-- This correctly aliases the REST Framework views

urlpatterns = [
    # API Authentication Token Endpoint
    path('token/', drf_views.obtain_auth_token, name='api_token_auth'),
    
    # Product API Endpoints (using your local 'views')
    path("products/", views.product_list, name="api_product_list"), 
    path("products/add/", views.product_add, name="api_product_add"), 
    path("products/update/<int:id>/", views.product_update, name="api_product_update"), 
    path("products/delete/<int:id>/", views.product_delete, name="api_product_delete"), 
]