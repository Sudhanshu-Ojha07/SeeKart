from django.urls import path
from home.views import index
from products.views import category_section





urlpatterns = [
   path('', index, name= 'index'),
   path('allcategories/<slug:category_slug>/', category_section, name ="category_section"),


    
]

