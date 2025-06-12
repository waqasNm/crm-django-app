from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, ProductForm, CreateUSerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUSerForm()
    if request.method == 'POST':
        form = CreateUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name="customer")
            user.groups.add(group)
            Customer.objects.create(user=user)

            messages.success(request,'Account was created for '+ username)
            return redirect('login')
    context = {'form':form}
    return render(request,'account/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username OR password is incorrect')
    context = {}
    return render(request,'account/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    
    context = {'orders':orders, 'customers':customers,
            "total_customers":total_customers,
            "total_orders":total_orders,
              "delivered":delivered,
                        "pending":pending          }
    return render(request,'account/dashboard.html',context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {'orders':orders,
               "total_orders":total_orders,
              "delivered":delivered,
                        "pending":pending}
    return render(request,'account/user.html',context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def products(request):
    allProducts = Product.objects.all()
    return render(request,'account/products.html',{"products":allProducts})

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    
    context = {
        'customer':customer,
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter}
    return render(request,'account/customer.html',context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    customer = Customer.objects.get(id=pk)
    OrderFormSet = inlineformset_factory(Customer,Order,
                                         fields=('product','status'),extra=2)
    # form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        # print("printing",request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        print(formset)
        if formset.is_valid:
            formset.save()
            return redirect('/')
        else:
            print("error submitting form")
    context = {'formset':formset}
    return render(request,'account/order_form.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'account/order_form.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {"order":order}

    return render(request,'account/delete.html',context)



# def updateProduct(request,pk):
#     product = Product.objects.get(id=pk)
#     form = ProductForm(instance=product)
#     if request.method == 'POST':
#         form = ProductForm(request.POST,instance=product)
#         if form.is_valid:
#             form.save()
#             return redirect('/customer/')
        
#         context = {"form":form}
#         return render(request,'account/product_form.html',context)


