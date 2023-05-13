from django.shortcuts import render,redirect
from .models import BuyerRegister,SellerRegister,Product_Category,Product,Contactus,Biddetails,pyment
from .form import BuyerRegisterForm,SellerRegisterForm
from datetime import date
# Create your views here.
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.core.mail import send_mail


    
def SessionData(request):
    biddata=Biddetails.objects.filter(status=False) & Biddetails.objects.filter(action=False)
    cDate = date.today()
    for i in biddata:
        s=[]
        abc=Biddetails.objects.filter(productID=i.productID)
        for k in abc:
            s.append(k.bidamount)
        productdata=Product.objects.get(id=i.productID)
        if cDate > productdata.enddate:
            for c in s:
                if max(s)==c:
                    print("max",c)
                    a=Biddetails.objects.filter(productID=i.productID)&Biddetails.objects.filter(bidamount=c)
                    for r in a:
                        r.status=True
                        r.action=True
                        r.save()
                        p=Product.objects.get(pk=r.productID)
                        p.status=True
                        p.save()
                else:
                    print("less",c)
                    a=Biddetails.objects.filter(productID=i.productID)&Biddetails.objects.filter(bidamount=c)
                    for r in a:
                        r.action=True
                        r.save()

def Mail(request):
    a=BuyerRegister.objects.filter(status=True) & BuyerRegister.objects.filter(mailsend=False)
    b= SellerRegister.objects.filter(status=True) & SellerRegister.objects.filter(mailsend=False)
    print("datamail",a)
    print("datamail",b)
    if len(a)>0:
        for i in a:
            data=BuyerRegister.objects.get(email=i.email)
            send_mail(
                        'Authentivation mail from Diamond Bid ',
                        'dear +(i.email)\n,Now You are account is verified by Diamond Bid  ',
                        'subhashdantani98@gmail.com',  # TODO: Update this with your mail id
                        [i.email],  # TODO: Update this with the recipients mail id
                        fail_silently=False,
                    )
            data.mailsend=True
            data.save()
    if len(b)>0:
        for i in b:
            data=SellerRegister.objects.get(email=i.email)
            send_mail(
                        'Dear : '+str(i.email),
                        'Now You are  verified persion  ',
                        'subhashdantani98@gmail.com',  # TODO: Update this with your mail id
                        [i.email],  # TODO: Update this with the recipients mail id
                        fail_silently=False,
                    )
            data.mailsend=True
            data.save()


def index(request):
    sData = SessionData(request) 
    mData = Mail(request) 
    if request.session.has_key('buyer'):       
        user= request.session['buyer']
        data=BuyerRegister.objects.get(email=user)
        productdata=Product.objects.filter(status=False)
        return render (request,'index.html',{'sessionbuyer':user,'name':data,'productdata':productdata})
    elif request.session.has_key('seller'):
        vendor= request.session['seller']
        data=SellerRegister.objects.get(email=vendor)
        productdata=Product.objects.filter(SellerId=request.session['sellerId']) & Product.objects.filter(status=False)    
        return render (request,'index.html',{'sessionseller':vendor,'name':data,'productdata':productdata})
    else:
        productdata=Product.objects.filter(status=False)
        return render (request,'index.html',{'productdata':productdata})

def diamonds(request):
    sData = SessionData(request)
    if request.session.has_key('buyer'):       
        user= request.session['buyer']
        data=BuyerRegister.objects.get(email=user)
        category=Product_Category.objects.all()
        productdata= Product.objects.filter(status=False)
        return render (request,'Diamonds.html',{'sessionbuyer':user,'name':data,'ab':category,'productdata':productdata})
    elif request.session.has_key('seller'):
        vendor= request.session['seller']
        data=SellerRegister.objects.get(email=vendor)
        category=Product_Category.objects.all()
        productdata=Product.objects.filter(SellerId=request.session['sellerId']) & Product.objects.filter(status=False)
        if request.method=="POST" and request.FILES['productImage']:
            seller_id=request.session['sellerId']
            category1=Product_Category.objects.get(id=request.POST['product_category'])
            name = request.POST['productname']
            price=request.POST['productPrice']
            quantity=request.POST['productQuantity']
            discription=request.POST['discription']
            img=request.FILES['productImage']
            startdate=request.POST['startdate']
            enddate=request.POST['enddate']                     
            Product.objects.create(SellerId=seller_id,category=category1,productName=name,productPrice=price,productDescription=discription,productImage=img,quantity=quantity,startdate=startdate,enddate=enddate)       
        return render (request,'Diamonds.html',{'sessionseller':vendor,'name':data,'ab':category,'productdata':productdata})
    else:
        category=Product_Category.objects.all()
        productdata=Product.objects.filter(status=False)
        return render (request,'Diamonds.html',{'ab':category,'productdata':productdata})
    
def productcat(request,id):
    sData = SessionData(request)
    if request.session.has_key('buyer'):       
        user= request.session['buyer']
        data=BuyerRegister.objects.get(email=user)
        category=Product_Category.objects.all()
        productdata=Product.objects.filter(category=id) & Product.objects.filter(status=False)
        return render (request,'Diamonds.html',{'sessionbuyer':user,'name':data,'ab':category,'productdata':productdata})
    elif request.session.has_key('seller'):
        vendor= request.session['seller']
        category=Product_Category.objects.all()
        data=SellerRegister.objects.get(email=vendor)
        if request.method=="POST" and request.FILES['productImage']:
            seller_id=request.session['sellerId']
            category1=Product_Category.objects.get(id=request.POST['product_category'])
            name = request.POST['productname']
            price=request.POST['productPrice']
            quantity=request.POST['productQuantity']
            discription=request.POST['discription']
            img=request.FILES['productImage']
            startdate=request.POST['startdate']
            enddate=request.POST['enddate']                     
            Product.objects.create(SellerId=seller_id,category=category1,productName=name,productPrice=price,productDescription=discription,productImage=img,quantity=quantity,startdate=startdate,enddate=enddate)
        productdata=Product.objects.filter(SellerId=request.session['sellerId']) & Product.objects.filter(category=id)& Product.objects.filter(status=False)
        return render (request,'Diamonds.html',{'sessionseller':vendor,'name':data,'ab':category,'productdata':productdata})
    else:
        category=Product_Category.objects.all()
        productdata=Product.objects.filter(category=id) & Product.objects.filter(status=False)
        return render (request,'Diamonds.html',{'ab':category,'productdata':productdata})

def contact(request):
    sData = SessionData(request)
    if request.session.has_key('buyer'):       
        user= request.session['buyer']
        data=BuyerRegister.objects.get(email=user)
        if request.method=="POST":
            model=Contactus()
            model.name=request.POST['name']
            model.email=request.POST['email']
            model.number=request.POST['number']
            model.message=request.POST['message']
            model.save()
            return render (request,'contact.html',{'sessionbuyer':user,'name':data,'messagekey':'message sent'})
        return render (request,'contact.html',{'sessionbuyer':user,'name':data,})
    elif request.session.has_key('seller'):
        vendor= request.session['seller']
        data=SellerRegister.objects.get(email=vendor)
        if request.method=="POST":
            model=Contactus()
            model.name=request.POST['name']
            model.email=request.POST['email']
            model.number=request.POST['number']
            model.message=request.POST['message']
            model.save()
            return render (request,'contact.html',{'sessionseller':vendor,'name':data,'messagekey':'message sent'})
        return render (request,'contact.html',{'sessionseller':vendor,'name':data})
    else:
        if request.method=="POST":
            model=Contactus()
            model.name=request.POST['name']
            model.email=request.POST['email']
            model.number=request.POST['number']
            model.message=request.POST['message']
            model.save()
            return render (request,'contact.html',{'messagekey':'message sent'})
        return render (request,'contact.html')

def about(request):
    sData = SessionData(request)
    if request.session.has_key('buyer'):       
        user= request.session['buyer']
        data=BuyerRegister.objects.get(email=user)
        # category=Product_Category.objects.all()
        return render (request,'about.html',{'sessionbuyer':user,'name':data})
    elif request.session.has_key('seller'):
        vendor= request.session['seller']
        data=SellerRegister.objects.get(email=vendor)
        # category=Product_Category.objects.all()       
        return render (request,'about.html',{'sessionseller':vendor,'name':data})
    else:
        # category=Product_Category.objects.all()
        return render (request,'about.html')

def buyersignin(request):
    sData = SessionData(request)
    if request.POST:
        email = request.POST['email']
        pass1 = request.POST['password']
        try:
            valid = BuyerRegister.objects.get(email=email,password=pass1)
            if valid.status==True:
                if valid:
                    request.session['buyer'] = email
                    request.session['name'] = valid.name
                    request.session['contactno'] = valid.number
                    request.session['user_address'] = valid.address
                    request.session['userId'] = valid.pk
                    return redirect('index')
            else:
                return render(request,'buyersignin.html',{'messagekey':'After varification you are able to log-in into system'})
        except:
            return render(request,'buyersignin.html',{'messagekey':'Password incorrect'})
    return render(request,'buyersignin.html')

def buyerlogout(request):
    if 'buyer' in request.session.keys():
        del request.session['buyer']
        return redirect('buyersignin')
    return redirect('buyersignin')

def buyersignup(request):
    sData = SessionData(request)
    obj=BuyerRegisterForm(request.POST,request.FILES) 
    if obj.is_valid():
        data=BuyerRegister.objects.all().filter(email=request.POST['email'])
        if len(data)<=0:
            if request.POST['password']==request.POST['password1']:
                obj.save()
                return redirect('buyersignin')
            else:
                return render(request,'buyersignup.html',{'messagekey':"Conferm The Right Password"})
        else:
            return render(request,'buyersignup.html',{'messagekey':"User Already Exists"})
    return render(request,'buyersignup.html')

def sellersignin(request):
    sData = SessionData(request)
    if request.POST:
        email = request.POST['email']
        pass1 = request.POST['password']
        try:
            valid = SellerRegister.objects.get(email=email,password=pass1)
            if valid.status==True:
                if valid:
                    request.session['seller'] = email
                    request.session['name'] = valid.name
                    request.session['contactno'] = valid.number
                    request.session['address'] = valid.address
                    request.session['sellerId'] = valid.pk
                    return redirect('index')
            else:
                return render(request,'sellersignin.html',{'messagekey':'After varification you are able to log-in into system'})
        except:
            return render(request,'sellersignin.html',{'messagekey':'Password incorrect'})
    
    return render(request,'sellersignin.html')

def sellerlogout(request):
    if 'seller' in request.session.keys():
        del request.session['seller']
        return redirect('sellersignin')
    return redirect('sellersignin')

def sellersignup(request):
    sData = SessionData(request)
    obj=SellerRegisterForm(request.POST,request.FILES) 
    if obj.is_valid():
        data=SellerRegister.objects.all().filter(email=request.POST['email'])
        if len(data)<=0:
            if request.POST['password']==request.POST['password1']:
                obj.save()
                return redirect('sellersignin')
            else:
                return render(request,'sellersignup.html',{'messagekey':"Conferm The Right Password"})
        else:
            return render(request,'sellersignup.html',{'messagekey':"User Already Exists"})
    return render(request,'sellersignup.html')

def singleproduct(request,id): 
    sData = SessionData(request) 
    if request.session.has_key('BID'):
        message = request.session['BID']
        del request.session['BID']
    else:
        message = ''
   
    if request.session.has_key('buyer'): 
             
        user= request.session['buyer']
        data=BuyerRegister.objects.get(email=user)
        productdata=Product.objects.get(id=id)
        cDate = date.today()
        biddata=Biddetails.objects.filter(productID=id).order_by("-id")
        bidtable=[]
        for i in biddata:
            buyer=BuyerRegister.objects.get(id=i.buyerId)
            d={
                'name':buyer.name,
                'bidamt':i.bidamount,
                'discription':i.Description,
                'date':i.date_of_bid
                }
            bidtable.append(d)    
        if request.method=="POST":
            model=Biddetails()
            model.productID=id
            model.SellerId=productdata.SellerId
            model.buyerId=request.session['userId']
            model.bidamount=request.POST['bidamount']
            model.Description=request.POST['Description']
            bidamt1=Biddetails.objects.filter(productID=id)&Biddetails.objects.filter(bidamount=model.bidamount)
            if cDate <= productdata.enddate:
                if len(bidamt1)==0:
                    model.save()
                    request.session['BID'] = "BID Amount"
                    return redirect('singleproduct', id=id)
                else:
                    return render (request,'singleproduct.html',{'sessionbuyer':user,'name':data,'productdata':productdata,'biddata':bidtable,'messagekey':"Bid amount alredy exists"})
            else:
                    return render (request,'singleproduct.html',{'sessionbuyer':user,'name':data,'productdata':productdata,'biddata':bidtable,'messagekey':"date gone"})
            
        return render (request,'singleproduct.html',{'sessionbuyer':user,'name':data,'productdata':productdata,'biddata':bidtable,'messagekey':message})
    elif request.session.has_key('seller'):
        vendor= request.session['seller']
        data=SellerRegister.objects.get(email=vendor)
        productdata=Product.objects.get(id=id)
        biddata=Biddetails.objects.filter(productID=id).order_by("-id")
        bidtable=[]
        for i in biddata:
            buyer=BuyerRegister.objects.get(id=i.buyerId)
            d={
                'name':buyer.name,
                'bidamt':i.bidamount,
                'discription':i.Description,
                'date':i.date_of_bid
            }
            bidtable.append(d)
        return render (request,'singleproduct.html',{'sessionseller':vendor,'name':data,'productdata':productdata,'biddata':bidtable})
        
    else:
        productdata=Product.objects.get(id=id)    
        biddata=Biddetails.objects.filter(productID=id).order_by("-id")
        bidtable=[]
        for i in biddata:
            buyer=BuyerRegister.objects.get(id=i.buyerId)
            d={
                'name':buyer.name,
                'bidamt':i.bidamount,
                'discription':i.Description,
                'date':i.date_of_bid
            }
            bidtable.append(d)
        return render (request,'singleproduct.html',{'productdata':productdata,'biddata':bidtable})

def sellerorder(request):
    sData = SessionData(request)
    if request.session.has_key('seller'):
        vendor= request.session['seller']
        data=SellerRegister.objects.get(email=vendor) 
        order=Biddetails.objects.filter(SellerId=request.session['sellerId'])&Biddetails.objects.filter(status=True)
        orderdata=[]
        for i in order:
            b=BuyerRegister.objects.get(id=i.buyerId)
            c=Product.objects.get(id=i.productID)
            d={
                'orderid':i.pk,
                'buyername':b.name,
                'productname':c.productName,
                'productamt':c.productPrice,
                'productdic':c.productDescription,
                'prouctimg':c.productImage,
                'bidamt':i.bidamount,
                'dateofbid':i.date_of_bid,
                'pyment':i.payment,
            }    
            orderdata.append(d)
        return render (request,'sellerorder.html',{'sessionseller':vendor,'name':data,'orderdata':orderdata})
    else:  
        return redirect('sellersignin')

def buyerorder(request):
    sData = SessionData(request)
    if request.session.has_key('buyer'):       
        user= request.session['buyer']
        data=BuyerRegister.objects.get(email=user)
        order=Biddetails.objects.filter(buyerId=request.session['userId'])&Biddetails.objects.filter(status=True)
        orderdata=[]
        for i in order:
            b=BuyerRegister.objects.get(id=i.buyerId)
            c=Product.objects.get(id=i.productID)
            d={
                'orderid':i.pk,
                'buyername':b.name,
                'productname':c.productName,
                'productamt':c.productPrice,
                'productdic':c.productDescription,
                'prouctimg':c.productImage,
                'bidamt':i.bidamount,
                'dateofbid':i.date_of_bid,
                'pyment':i.payment,
            }    
            orderdata.append(d)
        return render (request,'buyerorders.html',{'sessionbuyer':user,'name':data,'orderdata':orderdata})
    else:  
        return redirect('buyersignin')



def direct_buy(request,id):
    if request.session.has_key('buyer'):       
        data=Biddetails.objects.get(id=id)             
        request.session['productID'] = data.productID
        request.session['SellerId'] = data.SellerId
        request.session['buyerId'] = data.buyerId
        request.session['orderAmount'] = data.bidamount
        request.session['shippingPaymentVia'] = "Online"
        request.session['shippingPaymentMethod'] = "Razorpay"
        request.session['shippingTransactionId'] = ""
        return redirect('razorpayView')                   
    else:
        return redirect('buyersignin')



RAZOR_KEY_ID = 'rzp_test_8iwTTjUECLclBG'
RAZOR_KEY_SECRET = '0q8iXqBL1vonQGVQn4hK1tYg'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['orderAmount'])*100
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'razorpayDemo.html',context=context)

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            amount = int(request.session['orderAmount'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)
            print("ram ram")
            #Order Save Code
            orderModel = pyment()
            orderModel.productID = (request.session['productID'])
            orderModel.SellerId = (request.session['SellerId'])
            orderModel.buyerId = (request.session['buyerId'])
            orderModel.orderAmount = str(request.session['orderAmount'])
            orderModel.paymentVia = request.session['shippingPaymentVia']
            orderModel.paymentMethod = request.session['shippingPaymentMethod']
            orderModel.transactionId = payment_id
            orderModel.save()
            print("ram ram")
            data=Biddetails.objects.filter(productID=request.session['productID'])
            for i in data:
                i.payment=True
                i.save()
            del request.session['productID']
            del request.session['SellerId']
            del request.session['buyerId']
            del request.session['orderAmount']
            del request.session['shippingPaymentVia']
            del request.session['shippingPaymentMethod']
            print("ram ram")
            # render success page on successful caputre of payment
            return redirect('buyerorder')
        except:
            print("Hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("Hello1")
       # if other than POST request is made.
        return HttpResponseBadRequest()