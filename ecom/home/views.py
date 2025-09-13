from django.shortcuts import render
from products.models import Product, Category

# Create your views here.
# def index(request):
#     context= {'products': Product.objects.all()}
#     return render(request, 'home/index.html', context)
def index(request):
    context = {'section': Category.objects.all()}
    return render(request, 'home/index.html', context)