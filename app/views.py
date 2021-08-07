from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Customer,OrderPlaced,Cart
from .forms import CustomerRegistrationForm,CustomerProfileForm,UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random 
import http.client
from django.conf import settings
class ProductView(View):
    def get(self,request):
        table=Product.objects.filter(category='T')
        chair=Product.objects.filter(category='C')
        sofa=Product.objects.filter(category='S')
        
        return render(request,'app/index.html',{'table':table,'chair':chair,'sofa':sofa})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_in_cart=False
        if request.user.is_authenticated:
            item_in_cart=Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
        
        return render(request,'app/productdetail.html',{'product':product,'item_in_cart':item_in_cart})

@login_required
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=150.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        
        for p in cart_product:
                temp=(p.quantity *p.product.selling_price)
                amount+=temp
                total_amount=amount+shipping_amount
        data ={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':total_amount
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quantity>1:
              c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=150.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        
        for p in cart_product:
                temp=(p.quantity *p.product.selling_price)
                amount+=temp
                
        data ={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
       
        c.delete()
        amount=0.0
        shipping_amount=150.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        
        for p in cart_product:
                temp=(p.quantity *p.product.selling_price)
                amount+=temp
                
        data ={
            
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)
@login_required
def remove_add(request,pk):
    address=Customer.objects.get(id=pk)
    address.delete()
    return redirect('address')
        
        
       
@login_required
def add_to_cart(request):
 user=request.user 
 product_id=request.GET.get('prod_id')
 
 products=Product.objects.get(id=product_id)
 
 cart_product=[p for p in Cart.objects.all() if p.user==user]
 if len(cart_product)<5:
    if cart_product:
            for p in cart_product:
                  
                  if p.product.id==products.id:
                         
                         return redirect('/cart')
            Cart(user=user,product=products).save()
            return redirect('/cart')
    else:
       Cart(user=user,product=products).save()
       return redirect('/cart')
 else:
     messages.success(request,"cart is full")
     return redirect('/cart')
            
#  cart_product=[p for p in Cart.objects.all() if p.user==user]
#  if cart_product:
#      for p in cart_product:
#           if  product_id == p.id:
#               plus_cart(request)
#               return redirect('/cart')
          
#      Cart(user=user,product=products).save()
#  else:


#  cartprod=Cart.objects.filter(user=user)
#  if product_id not in cartprod.product.id:
 
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=150.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                temp=(p.quantity *p.product.selling_price)
                amount+=temp
                total_amount=amount+shipping_amount
        return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})


@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
 add=Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-dark'})

@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'op':op})



def table(request):
 
    table=Product.objects.filter(category='T')
    return render(request, 'app/table.html',{'table':table})

def sofa(request):
 
    sofa=Product.objects.filter(category='S')
    return render(request, 'app/sofa.html',{'sofa':sofa})
def chair(request):
    chair=Product.objects.filter(category="C")
    return render(request,'app/chair.html',{'chair':chair})
def payment(request):
    pass


# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def  get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        # otp=str(random.randint(1000,999))
        if form.is_valid():
            messages.success(request,'Registered Successfully!!')
            form.save()
            return redirect('login')
        else:


            return render(request,'app/customerregistration.html',{'form':form})
# def otp(request):
#         return render(request,'otp.html')
# def send_otp(phone,otp):
#     payload = "{\"Value1\":\"Param1\",\"Value2\":\"Param2\",\"Value3\":\"Param3\"}"
#     authkey=settings.authkey
#     headers = { 'content-type': "application/json" }

#     url="https://control.msg91.com/api/sendotp.php?otp"+otp+'&sender=ABC&message='+'Your otp is '+otp +'&mobile='+phone+'&authkey=&country=+91'


@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart_items=Cart.objects.filter(user=user)
    
    
    amount=0.0
    shipping_amount=150.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==user]
    if cart_product:
            for p in cart_product:
                temp=(p.quantity *p.product.selling_price)
                amount+=temp
            total_amount=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':total_amount,'amount':amount,'cart_items':cart_items})

@login_required
def paymentdone(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,Customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")



def redirect_view(request):
    response = redirect('/app/login.html/')
    return response

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-dark'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            phone=form.cleaned_data['phone']
            reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode,phone=phone)
            reg.save()
            # messages.success(request,' Profile Saved !!')
            # messages.success(request,'Profile Saved!!')
            # form.save()
            return redirect('index')
        else:
           return render(request,'app/profile.html',{'form':form})

