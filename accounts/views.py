from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

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

def customers(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    context = {'customer':customer, 'orders':orders}
    return render(request, 'accounts/customers.html',context)


def createOrder(request):

    context={}
    return render(request,'accounts/order_form.html',context)
