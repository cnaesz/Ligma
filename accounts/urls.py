from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('user/', views.userPage, name='user-page'),
    path('register/', views.registerPage, name='register'),
    path('account/', views.accountSetting, name='account'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('products/', views.products, name='products'),
    path('customers/<str:pk_test>/', views.customers, name='customers'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('create_customer/', views.createCustomer, name='create_customer'),
    path('create_product/<str:pk>/', views.createProduct, name='create_product'),

]
