
from django.shortcuts import render,redirect
from store.models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.http import HttpResponse
from accounts.views import*

@never_cache

def home(request):
    if 'key1' in request.session:
      
      profile = request.session.get('profile')
      products=Product.objects.all().filter(is_available=True)
      context = {'profile': profile,'products':products}
      return render(request,'home.html',{'products': products, 'profile': profile}) 
  
   
    products=Product.objects.all().filter(is_available=True)
    context={
        'products':products
    }
    return render(request, 'home.html',context)
