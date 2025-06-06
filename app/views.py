from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

# def home(request):
#  return render(request, 'app/home.html')

class productView (View):
 def get(self, request):
  TopWear = Product.objects.filter(category='TW')
  BottomWear = Product.objects.filter(category='BW')
  Mobile = Product.objects.filter(category='M')
  Laptop = Product.objects.filter(category='L')
  return render (request, 'app/home.html', {'topwear':TopWear,'bottomwear':BottomWear,'mobile':Mobile,'laptop':Laptop})

class productDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/productdetail.html', {'product':product})

def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 cart = Cart(user=user, product=product)
 cart.save()
 return redirect('/cart')

def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)

  amount = 0.0
  shipping_amount = 99.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user==user]

  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shipping_amount
 
 return render (request, 'app/addtocart.html', {'carts':cart, 'totalamount':total_amount, 'amount':amount, 'shippingcost':shipping_amount})

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add, 'active':'btn-primary'})

def orders(request):
 order = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order':order})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Samsung' or data == 'Redmi':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=50000) 
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=50000)

 return render(request, 'app/mobile.html', {'mobiles':mobiles})

def topwear (request, data=None):
 if data == None:
  topwear = Product.objects.filter(category='TW')
 elif data == 'Levis' or data == 'Nike':
  topwear = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
  topwear = Product.objects.filter(category='TW').filter(discounted_price__lt=1000)
 elif data == 'above':
  topwear = Product.objects.filter(category='TW').filter(discounted_price__gt=1000)

 return render (request,'app/topwear.html', {'topwear':topwear})


def bottomwear (request, data=None):
 if data == None:
  bottomwear = Product.objects.filter(category='BW')
 elif data == 'Levis' or data == 'Addidas':
  bottomwear = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
  bottomwear = Product.objects.filter(category="BW").filter(discounted_price__lt = 1000)
 elif data == 'above':
  bottomwear = Product.objects.filter(category="BW").filter(discounted_price__gt = 1000)
 return render (request,'app/bottomwear.html', {'bottomwear':bottomwear})

def login(request):
 return render(request, 'app/login.html')

class customerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})
 
 def post (self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   form.save()
   messages.success(request, "Registered Successfully!! Login now")
  else:
   messages.error(request,"Please fill out all the fields correctly!")
  return render (request, 'app/customerregistration.html', {'form':form})
 
def checkout(request):
 user = request.user
 address = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_cost = 99.0 
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
  totalamount = amount + shipping_cost
 return render(request, 'app/checkout.html', {'add':address, 'totalamount':totalamount, 'cartitems':cart_items})

def paymentdone(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
   OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
   c.delete()
  return redirect('orders')

class CustomerProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render (request, 'app/profile.html', {'form':form,'active':'btn-primary'})
 
 def post (self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr,   name=name, locality=locality, city=city, zipcode=zipcode, state=state )
   reg.save()
   messages.success(request,'Congratulations!! Profile Updated successfully.')

   return render (request,'app/profile.html',{'form':form,'active':'btn-primary'})

def plus_cart (request):
  if request.method == "GET":
   prod_id = request.GET['prod_id']
   print("PRODUCRRRRR",prod_id)
   c = Cart.objects.filter( Q(product=prod_id) & Q(user=request.user)).first()
   c.quantity+=1
   c.save()
   amount = 0.0
   shipping_price = 99.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user  ]

   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount

  data = {
      'quantity': c.quantity,
      'amount': amount,
      'total_amount': amount + shipping_price
        }
  return JsonResponse(data)


def minus_cart(request):
  if request.method == "GET":
   prod_id = request.GET['prod_id']
   print("PRODUCRRRRR",prod_id)
   c = Cart.objects.filter( Q(product=prod_id) & Q(user=request.user)).first()
   c.quantity-=1
   c.save()
   amount = 0.0
   shipping_price = 99.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user  ]

   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount

  data = {
      'quantity': c.quantity,
      'amount': amount,
      'total_amount': amount + shipping_price
        }
  return JsonResponse(data)

def remove_cart(request):
  if request.method == "GET":
   prod_id = request.GET['prod_id']
   print("PRODUCRRRRR",prod_id)
   c = Cart.objects.get( Q(product=prod_id) & Q(user=request.user))
   c.delete()
   amount = 0.0
   shipping_price = 99.0
   cart_product = [p for p in Cart.objects.all() if p.user == request.user  ]

   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount


  data = { 
      'amount': amount,
      'total_amount': amount + shipping_price
        }
  return JsonResponse(data)
