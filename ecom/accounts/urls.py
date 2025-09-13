from django.urls import path
from . import views



urlpatterns = [
    path('login/', views.login_page, name ="login" ),
    path('register/', views.register_page, name= "register" ),
    path('logout/', views.logout_view, name='logout'),
    path("activate/<str:email_token>/", views.activate_account, name="activate_account"),
    path('cart/', views.cart, name='cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
    

    


