from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from accounts.models import Profile, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from products.models import Product, SizeVariant, ColorVariant
from django.views.decorators.cache import never_cache



# Create your views here.

@never_cache
def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)
        
        if not user_obj.exists():
            messages.warning(request, "Account not found.")
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified')
            return HttpResponseRedirect(request.path_info)
         

        user_obj = authenticate(username= email, password= password)
        if user_obj:
            login(request, user_obj)
            print(f"User '{user_obj.username}' logged in, session created.")  # Console debug

            return redirect('index')
        messages.warning(request, "Invalid credential")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/login.html')
@never_cache
def logout_view(request):
    logout(request)
    return redirect('index')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, "Email is already taken")
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(first_name=first_name, last_name= last_name, email=email, username=email) 
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, "An email has been sent on your provided mail.")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'accounts/register.html')




def activate_account(request, email_token):
    """
    Activate the account when the user clicks the email verification link.
    """
    try:
        profile = Profile.objects.get(email_token=email_token)
        if profile.is_email_verified:
            messages.warning(request, "Account already verified.")
            return redirect("login")
        else:
            profile.is_email_verified = True
            profile.email_token = None  # Clear the token after verification

            profile.save()
            messages.success(request, "Your account has been verified successfully.")
            return redirect("login")  # Redirect to login page
    except Profile.DoesNotExist:
        messages.error(request, "Invalid or expired token.")
        return redirect("register")  # Redirect to register page
    

def cart(request):
    if request.user.is_authenticated:
        cart = request.user.cart
        items = cart.items.all()
        return render(request, 'cart/cart.html', {'items': items})

   
    return render(request, 'cart/cart.html')

   
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
    item.delete()
    return redirect('cart')