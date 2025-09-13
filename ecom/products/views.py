from django.shortcuts import render, redirect
from products.models import Product,SizeVariant, ColorVariant, Category
from products.helper import product_size
from django.shortcuts import render, get_object_or_404
from accounts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required




# Create your views here.e
def category_section(request,category_slug):
    category = Category.objects.get(slug = category_slug)
    element = Product.objects.filter(category = category)
    context = {'allcategory': category, 'products': element}
    return render(request, 'product/allproduct.html',context )

def get_products(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)

        related_products = Product.objects.filter(category=product.category).exclude(uid=product.uid)
        product_size(slug)
        context= {'product': product, 'related_products': related_products}
        if request.GET.get('size') and product.has_size:
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size']= size
            context['updated_price'] = price
            print(price)
        return render(request, 'product/product.html', context= context)
    except Exception as e:
        print(e)
        return render(request, 'product/error.html', {'error': str(e)})
@login_required
def add_to_cart(request, product_uid):
    try:
        # Get the product
        product = get_object_or_404(Product, uid=product_uid)   #product = Product.objects.get(id=product_uid)

        # Get the user's cart
        cart = request.user.cart

        # Get size and color variants if selected
        size_variant = None
        color_variant = None

        if request.GET.get('size'):
            size_variant = SizeVariant.objects.get(size_name=request.GET.get('size'))

        if request.GET.get('color'):
            color_variant = ColorVariant.objects.get(color_name=request.GET.get('color'))

        # Check if the item is already in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size_variant=size_variant,
            color_variant=color_variant,
        )

        # If the item is already in the cart, increase the quantity
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')  # Redirect to the cart page
    except Exception as e:
        print(e)
        return redirect('get_products', slug=product.slug)
    
def cart_items(request):
    item= CartItem.objects.all()
    sum=len(item)
    
    context={'allitem': sum}
    return render(request, "base/base.html",context)
        
        

