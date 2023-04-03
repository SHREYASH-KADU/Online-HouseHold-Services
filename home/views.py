from django.shortcuts import render,redirect
from django.http import HttpResponse #manually added
from django.contrib.auth import authenticate,login,logout
from home.models import Contact,User ,Service,Worker#manually added to import database
from datetime import datetime #manually added
import razorpay
from getHelp.settings import razor_pay_key_id,razor_pay_key_secret
# Create your views here.

def login_view(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request,email=email ,password=password)
        
        if user is not None:  
            login(request,user)
            # Redirect to a success page.
            return redirect("/")
        else:       
            return render(request,"login.html" )

    services = Service.objects.all()
    context = {
        "services":services
    }
    return render(request,"login.html",context) # Return an 'invalid login' error message.

def logout_view(request):
    logout(request)
    return redirect("/login")

def register(request):
    if request.method=="POST":
        name = str(request.POST.get('name'))
        email = request.POST.get('email')
        password = request.POST.get('password')
        sign = request.POST.get('isWorker')
        is_worker = False
        if sign=='on':
            is_worker=True
        user = User.objects.create_user(name=name , email=email ,password=password,is_worker=is_worker)
        user.save()
        
        if is_worker:
            service_id = request.POST.get('service')
            service = Service.objects.get(id = service_id)
            worker = Worker(user=user,service = service)
            worker.save()

        return render(request,'login.html')
    
    return render(request,'login.html')

def index(request):
    if request.user.is_authenticated:
        services_list = Service.objects.all()
        context={
            "name":request.user.name,
            "services":services_list
        }
        return render(request,"index.html",context)

    return redirect("/login")

def dashboard(request):
    if request.user.is_authenticated:
        services_list = Service.objects.all()
        context={
            "services":services_list
        }
        return render(request,"dashboard.html",context)

    return redirect("/login")

def services(request,slug):
    if request.user.is_authenticated:
        service = Service.objects.get(slug=slug)
        context={
            'client' : User.objects.get(id=request.user.id),
            "workers" : Worker.objects.filter(service=service)
        }
        return render(request,"services.html",context)

    return redirect("/login")

def serviceDetails(request,service_slug,worker_id):
    if request.user.is_authenticated:
        context={
            'client' : User.objects.get(id=request.user.id),
            'worker' : Worker.objects.get(id=worker_id),
            'service' : Service.objects.get(slug=service_slug)      
        }
        return render(request,"serviceDetail.html",context)

    return redirect("/login")

        
client = razorpay.Client(auth=(razor_pay_key_id, razor_pay_key_secret))
def payment(request,service_slug,worker_id):  
    if request.user.is_authenticated:
        service = Service.objects.get(slug = service_slug)
        DATA = {
            "amount": int(service.wage)*100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2",
            },
            "payment_capture":1
        }

        payment_order = client.order.create(data=DATA)    

        worker = Worker.objects.get(id = worker_id)
        user = User.objects.get(id = request.user.id)

        context={
            "service":service,
            "worker" : worker,
            "user" : user,
            "api_key": razor_pay_key_id,
            "payment_order_id" : payment_order['id']
        }
        return render(request,"payment.html",context)

    return redirect("/login")

def last(request):
    if request.user.is_authenticated:
        return render(request,"last.html")

    return redirect("/login")
