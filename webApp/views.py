from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from .form import CustomeForm
from django.contrib.auth import login,logout,authenticate
import json
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta

def home(request):
    sliders = Slider.objects.filter(status=0)  # Filter active sliders
    products = Product.objects.filter(status=0, trending=1)
    return render(request, 'home.html', {'sliders': sliders,'trendP': products})




def register(request):
    if request.method == 'POST':
        form = CustomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Succesfully Completed You Can Login Now')
            return redirect('login')
        else:
        
            return render(request, 'register.html', {'form': form})
    else:
        
        form = CustomeForm()
        return render(request, 'register.html', {'form': form})
    
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully")
        return redirect('home')
def user_login(request):
    if request.method=='POST':
        name=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=name,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in Successfully")
            return redirect('home')
        else:
            messages.error(request,"Invalid Username or Password")
            return redirect('login')
    return render(request,'login.html')

def collection(request):
    category=Category.objects.filter(status=0)
    return render(request,'collections.html',{'category':category})

def collectionView(request,name):
    if Category.objects.filter(name=name,status=0):
       
        product=Product.objects.filter(category__name=name,status=0)
        return render(request,'product/index.html',{'product':product,'c':name})
    else:
        messages.warning(request,'No such Category found')
        return redirect('collections')
    
def productView(request,cname,pname):
    if (Category.objects.filter(name=cname,status=0)):
        if (Product.objects.filter(name=pname,status=0)):
            product=Product.objects.filter(name=pname).first()

            return render(request,'product/product.html',{'product':product})
        
def place_order(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_qty = data.get('product_qty')
            product_id = data.get('pid')
            name = data.get('name')
            number = data.get('number')
            alt_number = data.get('alt_number')
            address = data.get('address')
            payment_type = data.get('payment_type')

            try:
                product = Product.objects.get(id=product_id)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)

            if product.quantity >= product_qty:
                try:
                    total_amount=product.selling_price*product_qty
                    selling_price=product.selling_price
                    order = Orders.objects.get(user=request.user, product=product)
                    order.product_quantity += product_qty
                    order.save()
                    return JsonResponse({'message': 'Order updated successfully'}, status=200)
                except Orders.DoesNotExist:
                    Orders.objects.create(user=request.user, product=product, name=name,
                                          product_quantity=product_qty, number=number,
                                          alt_number=alt_number, address=address,
                                          payment_type=payment_type,
                                          selling_price=selling_price,
                                          total_amount=total_amount)
                    messages.success(request,f"Your Order was Successfully Placed {request.user.name}")
                    return JsonResponse({'message': 'Order placed successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Insufficient product quantity'}, status=400)
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=403)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            #request.user.id
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):

                    return JsonResponse({'status':'Product Alredy in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_quantity=product_qty)
                        messages.success(request,"Product Added to Cart Successfully")
                        return JsonResponse({'status':'Product Added to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    




            


def add_to_fav(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_id = data['pid']
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Fav.objects.filter(user=request.user,product_id=product_id):
                    return JsonResponse({'status':'Product Alredy in Favorite'},status=200)
                else:
                    Fav.objects.create(user=request.user,product_id=product_id)
                    messages.success(request,"Product Added to Favorite Successfully")
                    return JsonResponse({'status': 'Product added to favorites'}, status=200)
            else:
                return JsonResponse({'status': 'Missing product ID'}, status=400)
        else:
            return JsonResponse({'status': 'User not authenticated'}, status=403)
    else:
        return JsonResponse({'status': 'Invalid request method'}, status=405)


def cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user.id)
        return render(request,'cart.html',{'cart':cart})

    else:
        return redirect('home')
def fav(request):
    if request.user.is_authenticated:
        fav=Fav.objects.filter(user=request.user.id)
        return render(request,'fav.html',{'fav':fav})
    else:
        return redirect('home')
def order(request):
    if request.user.is_authenticated:
        order=Orders.objects.filter(user=request.user.id)
        order.dates
        return render(request,'user.html',{'order':order})
    
def remove_cart(request,cid):
    cartItem=Cart.objects.get(id=cid)
    cartItem.delete()
    return redirect('cart')

def remove_fav(request,fid):
    favItem=Fav.objects.get(id=fid)
    favItem.delete()
    return redirect('favorites')

def remove_order(request,oid):
    favItem=Orders.objects.get(id=oid)
    favItem.delete()
    return redirect('orders')




def search_view(request):
    query = request.GET.get('q', '')
    categories = Category.objects.filter(name__icontains=query)
    if categories.exists():
        category_products = Product.objects.filter(category__in=categories)
        return render(request, 'search_result.html', {'results': category_products,'query':query})
    else:
        products = Product.objects.filter(name__icontains=query)
        return render(request, 'search_result.html', {'results': products,'query':query})
    
def order_details(request, did):
    if request.user.is_authenticated:
        data = Orders.objects.get(id=did)
        delivery_date = data.date + timedelta(days=7)
        return render(request, 'order_details.html', {'data': data, 'delivery_date': delivery_date})

