from django.urls import path
from products.views import get_products, add_to_cart,cart_items


urlpatterns = [
    path('<slug>/', get_products, name ="get_products"),
    path('add-to-cart/<str:product_uid>/', add_to_cart, name='add_to_cart'),
    path('view-cart/', cart_items,name="cart_items"),
    

    
]

