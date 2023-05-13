from django.db import models

# Create your models here.

class BuyerRegister(models.Model):
    name=models.CharField(max_length=20,default='',verbose_name='User Name')
    email=models.EmailField(max_length=50,verbose_name='Email',default=None)
    number=models.IntegerField(default='',verbose_name='Contact No')
    gst_number=models.CharField(max_length=50,verbose_name='GST No')
    address=models.TextField(default=None)
    password=models.CharField(default=None,max_length=20,verbose_name='Password')
    status=models.BooleanField(default=False)
    mailsend=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class SellerRegister(models.Model):
    name=models.CharField(max_length=20,default='',verbose_name='User Name')
    email=models.EmailField(max_length=50,verbose_name='Email',default=None)
    number=models.IntegerField(default='',verbose_name='Contact No')
    Company_name=models.CharField(max_length=20,default='',verbose_name='Company Name')
    address=models.TextField(default=None)
    gst_number=models.CharField(max_length=50,verbose_name='GST No') 
    password=models.CharField(default=None,max_length=20,verbose_name='Password')
    status=models.BooleanField(default=False)
    mailsend=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Product_Category(models.Model):
    name=models.CharField(max_length=20,verbose_name='Category Name')
    img=models.ImageField(upload_to="Category")
    def __str__(self):
        return self.name

class Product(models.Model):
    SellerId=models.CharField(max_length=100)
    category = models.ForeignKey(Product_Category,on_delete=models.CASCADE)
    productImage = models.ImageField(upload_to="product")
    productName = models.CharField(max_length=100)
    productPrice = models.IntegerField(default=0)
    productDescription = models.TextField(default="")
    quantity=models.CharField(max_length=200)
    startdate=models.DateField(default=None)
    enddate=models.DateField(default=None)
    status=models.BooleanField(default=False)

    def __str__(self):
        return self.productName
class Contactus(models.Model):
    name=models.CharField(max_length=20,default='',verbose_name=' Name')
    email=models.EmailField(max_length=50,verbose_name='Email')
    number=models.CharField(max_length=20,default='',verbose_name=' Subject')
    message=models.TextField()
    def __str__(self):
        return self.name

class Biddetails(models.Model):
    productID=models.CharField(max_length=100,default='')
    SellerId=models.CharField(max_length=100)
    buyerId=models.CharField(max_length=100)
    bidamount=models.IntegerField(default='')
    Description=models.TextField(default=None)
    date_of_bid=models.DateField(auto_created=True,auto_now=True) 
    status=models.BooleanField(default=False)
    action=models.BooleanField(default=False)
    payment=models.BooleanField(default=False)
   
    def __str__(self):
        return self.productID

class pyment(models.Model):
    productID=models.CharField(max_length=100,default='')
    SellerId=models.CharField(max_length=100)
    buyerId=models.CharField(max_length=100)
    orderAmount = models.CharField(max_length=50)
    paymentVia = models.CharField(max_length=50 ,default="")
    paymentMethod = models.CharField(default=None,max_length=50)
    transactionId = models.TextField(default=None)
    orderDate = models.DateTimeField(auto_created=True,auto_now=True)
   
    def __str__(self):
        return self.productID