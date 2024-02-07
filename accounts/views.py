from django.shortcuts import render
from .forms import RegistrationForm,MessageHandler
from django.shortcuts import redirect
from .models import Account
from django.contrib import messages,auth
from .models import Profile
import random
from django.http import HttpResponse
import secrets
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User, Permission, Group
from django.shortcuts import get_object_or_404
from category.models import Category
from category.forms import CategoryForm
from store.models import Product,ProductImage,Variation
from store.forms import ProductForm,AdditionalImageForm,VariantForm
from django.forms import formset_factory
from django.forms import modelformset_factory
from carts.models import Cart,CartItem
from carts.views import _cart_id
import requests
from orders.models import Order,OrderProduct
from .forms import UserProfileForm,UserForm
from accounts.models import UserProfile,Address
from orders.forms import ChangeStatusForm
from django.utils.crypto import get_random_string




#user registration
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def register(request):
  if 'key2' in request.session:
        del request.session['key2']
        return redirect('home')

  if request.method=='POST':
    form=RegistrationForm(request.POST)
    if form.is_valid():
      first_name=form.cleaned_data['first_name']
      last_name=form.cleaned_data['last_name']
      phone_number=form.cleaned_data['phone_number']
      email=form.cleaned_data['email']
      password=form.cleaned_data['password']
      user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,phone_number=phone_number)
      user.save()
      
      #user activation
      otp = ''.join(secrets.choice('0123456789') for _ in range(4))
      profile=Profile.objects.create(user=user,otp=f'{otp}')
      profile.save()
      user_details = {
            'uid':profile.uid,
            'phone_number':profile.user.phone_number,
            
        }
      request.session['user_details'] = user_details
      request.session['key2']=2
      messagehandler=MessageHandler(request.POST['phone_number'],otp).send_otp_via_message()
      red=redirect(f'otp/{profile.uid}/')
      red.set_cookie("can_otp_enter",True,max_age=60)
      return red  

      messages.success(request,'Registration Sucessful')
      return redirect('register')

  else:
    form=RegistrationForm
  context={
    'form':form
    }
  return render(request,'accounts/register.html',context)


#user login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def login(request):
  if 'key1' in request.session:
      
      profile = request.session.get('profile')
      products=Product.objects.all().filter(is_available=True)
      context = {'profile': profile,'products':products}
      return render(request,'home.html',{'products': products, 'profile': profile}) 
  if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        # Check if a profile with the given phone number exists
        user=Account.objects.filter(email=email).first()
        if not user:
            messages.error(request, "User does not exist.")
            return redirect('login')
        if not user.is_active:
            messages.error(request, "Your account has been temporarily blocked. Please contact support for further assistance.")
            return redirect('login')
        profile=Profile.objects.get(user=user)
        otp = ''.join(secrets.choice('0123456789') for _ in range(4))
        profile.otp=otp
        profile.save() 
        user_details = {
            'profile_email':profile.user.email,
            'phone_number':profile.user.phone_number, 
           }
        request.session['user_details'] = user_details
        request.session['key5']=5
        messagehandler = MessageHandler(profile.user.phone_number, otp).send_otp_via_message()
        red = redirect('otpVerify_login')
        red.set_cookie("can_otp_enter",True,max_age=60)
        return red       
  return render(request, 'accounts/login.html')

#login_otp_verify
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def otpVerify_login(request):
    if 'key1' in request.session:
      profile = request.session.get('profile')
      products=Product.objects.all().filter(is_available=True)
      context = {'profile': profile,'products':products}
      return render(request,'home.html',{'products': products, 'profile': profile}) 
    if request.method == "POST":
        try:
         profile = Profile.objects.get(otp=request.POST['otp'])
        except:
            messages.error(request, 'You have entered wrong OTP.Try again')
            return redirect(request.path)
        if request.COOKIES.get('can_otp_enter')!=None:  
            if profile.otp == request.POST['otp']:
                if profile.user is not None:
                   try:
                       cart=Cart.objects.get(cart_id=_cart_id(request))
                       is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                       if is_cart_item_exists:
                           cart_item=CartItem.objects.filter(cart=cart)
                           
                           #getting the product variation by cart id
                           product_variation=[]
                           for item in cart_item:
                               variation=item.variations.all()
                               product_variation.append(list(variation))
                           # get the cart items from the user to access his product variation
                           cart_item=CartItem.objects.filter(user=profile.user)
                           #check if current in exisring
                           ex_var_list=[]
                           id=[]
                           for item in cart_item:
                             existing_variation=item.variations.all()
                             ex_var_list.append(list(existing_variation))
                             id.append(item.id)
                            
                           for pr in product_variation:
                               if pr in ex_var_list:
                                   index=ex_var_list.index(pr)
                                   item_id=id[index]
                                   item=CartItem.objects.get(id=item_id)
                                   item.quantity +=1
                                   item.user=profile.user
                                   item.save()
                                
                               else:
                                   cart_item=CartItem.objects.filter(cart=cart)
                                   for item in cart_item:
                                      item.user=profile.user
                                      item.save()    
                   except:
                       pass
                   auth.login(request, profile.user)
                   profile.user.session = {'profile.user.id': profile.user.id}
                   profile.user.save()
                   profile={
                       'id':profile.id,
                       'first_name':profile.user.first_name
                   }
                   products=Product.objects.all().filter(is_available=True)
                   context = {'profile': profile,'products':products}
                   request.session['profile']=profile
                   request.session['key1']=1
                   return render(request,'home.html',{'products': products, 'profile': profile})
                return redirect('login')
            else:
              messages.error(request, 'You have entered wrong OTP.Try again')
              return redirect(request.path)
        messages.error(request,'60 seconds over.Try again')
        return redirect(request.path)
    return render(request, "accounts/otp_login.html")

#login_otp_resend
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def resend_otp_login(request):
 if 'resend_otp' in request.POST:
    user_details = request.session.get('user_details')
    if user_details:
        # Access user details from the session
             otp = ''.join(secrets.choice('0123456789') for _ in range(4))
             profile_email = user_details['profile_email']
             user=Account.objects.get(email=profile_email)
             profile=Profile.objects.get(user=user)
             profile.otp=otp
             profile.save()
             messagehandler=MessageHandler(profile.user.phone_number,otp).send_otp_via_message()
             red=redirect('otpVerify_login')
             red.set_cookie("can_otp_enter",True,max_age=60)
             messages.success(request, 'OTP has been resent')
             return red 
    return render(request, 'login.html')
 return render(request, 'accounts/login.html')  


def home1(request):
    if request.COOKIES.get('verified') and request.COOKIES.get('verified')!=None:
        messages.success(request, 'This is a success message.')
        return redirect("register")
    else:
        messages.error(request, 'This is an error message.')
        return redirect("register")

#user registration_otp_verify
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def otpVerify(request,uid):
    if'key3' in request.session:
        return redirect('register')
    if request.method == "POST":
        otp = request.POST.get('otp')
        try:
            profile = Profile.objects.filter(uid=uid).first()
        except Profile.DoesNotExist:
            return HttpResponse("Profile not found", status=404)
        if request.COOKIES.get('can_otp_enter')!=None:  
            if otp == profile.otp:
                if profile.user is not None:
                   profile.user.session = {'profile.user.id': profile.user.id}
                   profile.user.is_active=True
                   profile.user.save()
                   request.session['key3']=3
                   messages.success(request, 'Your Account has been activated.You can log in now')
                   return redirect("login")
                return redirect('register')
            messages.error(request, 'You have entered wrong OTP.Try again')
            return redirect(request.path)
        messages.error(request,'60 seconds over.Try again')
        return redirect(request.path)
    return render(request, "accounts/otp.html", {'uid': uid})

#userregistration_resend_otp
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def resend_otp(request):
  if 'resend_otp' in request.POST:
    user_details = request.session.get('user_details')
    if user_details:
            # Access user details from the session
             uid = user_details['uid']
             phone_number = user_details['phone_number']
          
             otp = ''.join(secrets.choice('0123456789') for _ in range(4))
             profile = Profile.objects.filter(uid=uid).first()
             profile.otp=otp
             profile.save()
             messagehandler=MessageHandler(profile.user.phone_number,otp).send_otp_via_message()
             red=redirect(f'register/otp/{profile.uid}/')
             red.set_cookie("can_otp_enter",True,max_age=60)
             messages.success(request, 'OTP has been resent')
             return red 
    return render(request, 'register.html')
  return render(request, 'accounts/register.html')  

#logout user
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
  if 'key1' in request.session:
        del request.session['key1']
  if 'user_details' in request.session:
        del request.session['user_details']     
  auth.logout(request)
  messages.success(request, 'Lougout Successful')
  return redirect('login')

#dashboard user
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dashboard(request):
    orders=Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count=orders.count()
    context={
        'orders_count':orders_count,
    }
    return render(request,'accounts/dashboard.html',context)

#admin login
@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_admin(request):
     if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard_admin')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login_admin')
     return render(request,'accounts/login_admin.html')

def dashboard_admin(request):
    return render(request,'admin/dashboard_admin.html')

#admin logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def logout_admin(request):
    auth.logout(request)
    messages.success(request, 'Lougout Successful')
    return redirect('login_admin')

#admin user list
def users_list(request):
    users_list = Account.objects.all()
    return render(request, 'admin/users_list.html', {'users_list' : users_list })

#user block and unblock
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def toggle_user_status(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('users_list')

#admin category lsit
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def category_list(request):
    category_list = Category.objects.all()
    return render(request, 'admin/category_list.html', {'category_list' : category_list})

#admin category add
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            slug = form.cleaned_data['slug']
            description = form.cleaned_data['description']
            cat_image = form.cleaned_data['cat_image']
            category = Category.objects.create(category_name=category_name, slug=slug, description=description, cat_image=cat_image)
            category.save()
            messages.success(request, 'Category Added Successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'admin/category_create.html', context)

#admin category update
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Updated Successfully.')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/category_update.html', {'form': form, 'category_id': category_id})

#admin category delete
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    category.is_available = not category.is_available
    category.save()
    messages.success(request, 'Category listing changed')
    return redirect('category_list')

#admin product list
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def product_list(request):
    product_list = Product.objects.all()
    return render(request, 'admin/product_list.html', {'product_list' : product_list})

#admin product add
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def product_add(request):
    ImageFormSet = modelformset_factory(ProductImage, form=AdditionalImageForm, extra=3)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.save()
            for form in formset.cleaned_data:
                if form:
                    addimage = form['addimage']
                    photo = ProductImage(product=product, addimage=addimage)
                    photo.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'admin/product_create.html', context)

#admin product update
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    ImageFormSet = modelformset_factory(ProductImage, form=AdditionalImageForm,extra=0,can_delete=True)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.filter(product=product))
        if form.is_valid() and formset.is_valid():
            form.save()
            for form in formset:
                if form.has_changed():
                    addimage = form.cleaned_data.get('addimage')
                    photo = form.save(commit=False)
                    photo.product = product
                    photo.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
        formset = ImageFormSet(queryset=ProductImage.objects.filter(product=product))
    context = {
        'form': form,
        'formset': formset,
        'product_id': product_id,
    }
    return render(request, 'admin/product_update.html', context)

#admin product delete
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    product.is_available= not product.is_available
    product.save()
    messages.success(request, 'Product listing changed.')
    return redirect('product_list')
 
#admin variant list
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def variant_list(request):
    variant_list = Variation.objects.all()
    return render(request, 'admin/variant_list.html', {'variant_list': variant_list})

#admin variant add
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def variant_add(request):
    if request.method == 'POST':
        form = VariantForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            variation_category = form.cleaned_data['variation_category']
            variation_value = form.cleaned_data['variation_value']
            variant = Variation.objects.create(product=product, variation_category=variation_category, variation_value=variation_value)
            variant.save()
            messages.success(request, 'Variant Added Successfully.')
            return redirect('variant_list')
    else:
        form = VariantForm()
    context = {
        'form': form
    }
    return render(request, 'admin/variant_create.html', context)

#admin variant update
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def variant_update(request, variant_id):
    variant = get_object_or_404(Variation, pk=variant_id)
    if request.method == 'POST':
        form = VariantForm(request.POST, instance=variant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Variant updated Successfully.')
            return redirect('variant_list')
    else:
        form = VariantForm(instance=variant)
    return render(request, 'admin/variant_update.html', {'form': form, 'variant_id': variant_id})

#admin variant delete
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def variant_delete(request, variant_id):
    variant_to_delete = Variation.objects.filter(id=variant_id)
    variant_to_delete.delete()
    messages.success(request, 'Variant deleted.')
    return redirect('variant_list')

#user order management
@login_required(login_url='login')
def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':orders,
    }
    return render(request,'accounts/my_orders.html',context)

#user edit profile
@login_required(login_url='login')
def edit_profile(request):
    userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method =="POST":
     user_form=UserForm(request.POST,request.FILES,instance=request.user)
     profile_form=UserProfileForm(request.POST,instance=userprofile)
     if user_form.is_valid() and profile_form.is_valid():
         user_form.save()
         profile_form.save()
         messages.success(request,'profile has been updated')
         return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
    context={
        'user_form':user_form,
        'profile_form':profile_form,  
    }
    return render(request,'accounts/edit_profile.html',context)

#user change password
@login_required(login_url='login')
def change_password(request):
    if request.method=="POST":
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        user=request.user
        if new_password==confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password changed sucessfully')
                return redirect('change_password')
            else:
                messages.error(request,'Please enter valid current Password')
                return redirect('change_password')
        else:
            messages.error(request,'Password does not match')
            return redirect('change_password')
    return render(request,'accounts/change_password.html')

#user order detail
@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context = {
        'order_detail' : order_detail,
        'order' : order,
        'subtotal' : subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)

#user cancel order
@login_required(login_url='login')
def cancel_order(request, order_id):
    user=request.user
    order_to_cancel= Order.objects.get(id=order_id)
    user.wallet+=order_to_cancel.order_total
    order_to_cancel.status='Cancelled'
    order_to_cancel.save()
    user.save()
    order_products = OrderProduct.objects.filter(order=order_to_cancel)
    for order_product in order_products:
     product = order_product.product
     quantity = order_product.quantity
    # Increase product stock by the canceled quantity
     product.stock += quantity
     product.save()
    return redirect('my_orders')

#user return order
@login_required(login_url='login')
def return_order(request, order_id):
    order_to_return= Order.objects.get(id=order_id)
    order_to_return.status='Return Requested'
    order_to_return.save()
    return redirect('my_orders')


@login_required(login_url='login_admin')
def cancel_order2(request, order_id):
    order_to_cancel= Order.objects.get(id=order_id)
    user=order_to_cancel.user
    user.wallet+=order_to_cancel.order_total
    order_to_cancel.status='Cancelled'
    order_to_cancel.save()
    user.save()
    order_products = OrderProduct.objects.filter(order=order_to_cancel)
    for order_product in order_products:
     product = order_product.product
     quantity = order_product.quantity
     product.stock += quantity
     product.save()
    return redirect('order_list_admin')


@login_required(login_url='login')
def address_list(request):
    address = Address.objects.filter(user=request.user,on_del=True)
    context = {
        'address' : address
    }
    return render(request, 'accounts/address_list.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def order_list_admin(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/order_list_admin.html', {'orders' : orders})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login_admin')
def change_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = ChangeStatusForm(request.POST, instance=order)
        if form.is_valid():
            # Get the current order status
            old_status = order.status
            # Save the form and get the new status
            form.save()
            new_status = form.cleaned_data['status']
            if new_status == "Return Received" or old_status == "Cancelled":
                user=order.user
                user.wallet+=order.order_total
                user.save()
            # Update product stock based on the new status
            update_product_stock(order, old_status, new_status)
            return redirect('order_list_admin')
    else:
        form = ChangeStatusForm(instance=order)
    return render(request, 'admin/change_order_status.html', {'form': form, 'order_id': order_id})

def update_product_stock(order, old_status, new_status):
    # Function to update product stock based on order status change
    if old_status == "Order Confirmed" and new_status == "Cancelled":
        # Order status changed from New to Cancelled, increase product stock
        for order_product in order.orderproduct_set.all():
            increase_stock(order_product.product, order_product.quantity)
    elif old_status == "Cancelled" and new_status == "Order Confirmed":
        # Order status changed from Cancelled to Accepted, decrease product stock
        for order_product in order.orderproduct_set.all():
            decrease_stock(order_product.product, order_product.quantity)
    elif  new_status == "Return Received":
        # Order status changed from New to Cancelled, increase product stock
        for order_product in order.orderproduct_set.all():
            increase_stock(order_product.product, order_product.quantity)


def increase_stock(product, quantity):
    # Function to increase product stock
    product.stock += quantity
    product.save()

def decrease_stock(product, quantity):
    # Function to decrease product stock
    if product.stock >= quantity:
        product.stock -= quantity
        product.save()


def forgot_password(request):
      if request.method=="POST":
        first_name=request.POST['first_name']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        try:
            user=Account.objects.get(email=email)
        except:
            return HttpResponse("User doesnt exist")
        otp = get_random_string(12)
        messagehandler = MessageHandler(user.phone_number, otp).send_otp_via_message()
        user.set_password(otp)
        user.save()
        logout(request)
        messages.success(request,'The code to reset your password has been sent to your mobile number.')
        return redirect('login')
      return render(request,'accounts/forgot_password.html')
   
    

