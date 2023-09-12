from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Product,Order,Design,Feedback
from django.contrib.auth import authenticate
# from django.contrib.auth.decorators import login_required

from django.contrib.admin.views.decorators import staff_member_required 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logouts

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer

from django.contrib import messages

from datetime import datetime

#mail
from django.core.mail import send_mail


# Create your views here.
def home(request):
    des=Design.objects.all()
    pros=Product.objects.all().filter(trending_product=True)
    feed=Feedback.objects.all().filter(show_in_page=True)
    data={"design":des,"pros":pros,"name":"Home","feeds":feed}
    return render(request,'home.html',data)

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def product(request):
    pros=Product.objects.all().order_by("product_name").values()
    data={"pros":pros,"name":"Product"} 
    return render(request,'product.html',data)

def order(request,pk):
    data=Order.objects.get(id=pk)
    # product split
    prods=data.products
    list=prods.split('\n')
    li=[]
    for i in list:
        li.append(i.split("-"))
    list=[]
    for i in li:
       list.append( {
            "product_name":i[0],
            "product_number":i[1],
            "product_size":i[2],
            "product_cost":i[3]
        })
    data.products=list
    
    return render(request,"order.html",{"data":data})

def query(request):
    return redirect("product")

def search(request):

    if request.method=="GET":
        val=request.GET.get("name").lower().capitalize()
        pros=Product.objects.all().filter(product_name__icontains=val)
    return render(request,"product.html",{"pros":pros,"name":"Product"})


# def sort(request):
#     pros=Product.objects.all().order_by("product_cost").values()
#     content={'pros':pros,"success":True}
#     return render(request,'product.html',content)

# ----------------------------------- change the data format and update the code in the above order function    
@api_view(['POST'])
def ordersuccess(request):
    dict=request.data
    time=str(datetime.now())
    li=time.split(".")
    dict["time"]= li[0]
    li=dict["products"].split(";")
    for i in range(len(li)-1):
        l=li[i].split("-")
        s=""
        s=l[0]+"-"+str(l[2])+"-("+str(l[1])+"kg)-"+"Rs."+l[3]
        li[i]=s
    print(li)
    dict["products"]='''                                                
'''.join(li)
    print(dict)
    serializer = OrderSerializer(data=dict)
    if serializer.is_valid():
        serializer.save()
    try:
        subject ="Dhanam recieved some new order"
        message = "A client has posted a feedback about their opinion. Check your admin site to know more"
        from_email = ''
        recipient_list = []
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print("error",e)

    return Response(serializer.data)
    

def feedback(request):
    return render(request,'feedback.html')

def feedbacksuccess(request):
    if request.method=="POST":
        name=request.POST.get("name").lower().capitalize()
        number=request.POST.get("contact")
        feedmsg=request.POST.get("feedback")
        data=Feedback(feedbacker_name=name,feedbacker_number=number,feedback=feedmsg,feedback_status=False) 
        data.save()
        try:
            subject ="Dhanam recieved some feedback"
            message =  name+" has posted a feedback about their opinion. Check your admin site to know more"
            from_email = ''
            recipient_list = []
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print("error",e)
        
        messages.success(request, "Feedback sent sucessfully")
        return redirect('home')
    else:
        return HttpResponse("<h2>Something went wrong</h2>")

def login(request):
    return render(request,'admin-login.html')

@staff_member_required
def loginsuccess(request):
    if request.method=="GET":
        return render(request,'adminpage.html')
    return HttpResponse("Error")


@staff_member_required
def feedbackdetails(request):
    data=Feedback.objects.all().filter(fstatus=False)
    return render(request,'feedback_details.html',{"datas":data})
    

@staff_member_required
def orderdetails(request):
    datas=Order.objects.all().filter(status=False)

    c=0
    for data in datas:
        c+=1
        prods=data.products
        list=prods.split(';')
        list.pop()
        li=[]
        for i in list:
            li.append(i.split("-"))
        list=[]
        for i in li:
            list.append( {
                "product_name":i[0],
                "product_number":i[1],
                "product_size":i[2],
                "product_cost":i[3]
            })
        data.products=list
    
    return render(request,'order_details.html',{"datas":datas})

def logout(request):
    if request.method=="POST":
        logouts(request)
        return redirect("home")
    
def verified(request,pk):
    if request.method=="POST":
        u=Feedback.objects.filter(id=pk).update(fstatus=True)
        data=Feedback.objects.all().filter(fstatus=False)
        
        messages.success(request, "The feddback is set to be noted")
        return redirect("details")

def delivered(request,pk):
    if request.method=="POST":
        u=Order.objects.filter(id=pk).update(status=True)
        data=Order.objects.all().filter(status=False)

        messages.success(request, "The order is set is be delivered")
        return redirect("orderdet")
