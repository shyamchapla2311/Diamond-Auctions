from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name="index"),
    path('diamonds/',diamonds,name="diamonds"),
    path('productcat/<int:id>',productcat,name="productcat"),
    path('contact/',contact,name="contact"),
    path('about/',about,name="about"),
    path('buyersignin/',buyersignin,name="buyersignin"),
    path('buyersignup/',buyersignup,name="buyersignup"),
    path('buyerlogout/',buyerlogout,name="buyerlogout"),
    path('sellersignin/',sellersignin,name="sellersignin"),
    path('sellersignup/',sellersignup,name="sellersignup"),
    path('sellerlogout/',sellerlogout,name="sellerlogout"),
    path('singleproduct/<int:id>',singleproduct,name="singleproduct"),
    path('sellerorder/',sellerorder,name="sellerorder"),
    path('buyerorder/',buyerorder,name="buyerorder"),
    path('direct_buy/<int:id>',direct_buy,name="direct_buy"),
    path('razorpayView/',razorpayView,name='razorpayView'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
    

    
]