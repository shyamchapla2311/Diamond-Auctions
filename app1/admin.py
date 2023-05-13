from django.contrib import admin
from .models import SellerRegister,BuyerRegister,Product_Category,Contactus,Product,Biddetails,pyment
# Register your models here.

admin.site.register(SellerRegister)
admin.site.register(BuyerRegister)
admin.site.register(Product_Category)
admin.site.register(Contactus)
admin.site.register(Product)
class bid(admin.ModelAdmin):
    list_display=['productID','bidamount','status','action']
admin.site.register(Biddetails,bid)
admin.site.register(pyment)