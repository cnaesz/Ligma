from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


from.decoration import *
from .filters import OrderFilter
from .models import *
from .forms import *
from .filters import *

# Create your views here.

@UnauthenticatedUser
def registerPage(request):
    form = CreateUserForm()
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context={'form':form}
    return render(request, 'accounts/register.html', context)

@UnauthenticatedUser
def loginPage(request):

    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context={}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@adminonly
def home(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    products = Product.objects.all()
    customers = Customer.objects.all()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'customers':customers, 'products':products, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs
    context = {'customer':customer, 'orders':orders, 'filter':filter}
    return render(request, 'accounts/customers.html',context)

@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method =='POST':
        formset=OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context={'formset':formset, 'customer':customer}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    context={'form':form, 'order':order}
    if request.method =='POST':
        form=OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method =='POST':
        order.delete()
        return redirect('home')

    context={'item':order}
    return render(request,'accounts/deleteOrder.html',context)

@login_required(login_url='login')
def createCustomer(request):
    form = CustomerForm(request.POST or None)
    if request.method =='POST':
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'accounts/customer_form.html',context)

@login_required(login_url='login')
def createProduct(request, pk):
    form = ProductForm(request.POST, instance=Product.objects.get(id=pk))
    if request.method =='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'accounts/customer_form.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def userPage(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSetting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    context = {'form':form}
    return render(request, 'accounts/account_setting.html', context)