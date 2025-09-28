from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views


from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Root URL: redirect based on login status
    path('', views.home_redirect, name='home_redirect'),  

    # Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='website/common/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('signup/', views.signup, name='signup'), 
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Product & Cart
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/review/', views.add_review, name='add_review'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'), 
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),

    # Search & API
    path('search/', views.search, name='search'),
    path('api/', include('website.api.urls')),
]



