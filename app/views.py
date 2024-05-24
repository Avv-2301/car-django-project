from django.shortcuts import render,redirect
from .models import Contact,Cars,Label,Team,Testimonial,Order
from django.core.paginator import Paginator
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .PayTm import Checksum
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
MERCHANT_KEY = 'uUXHfPG3u7Y5tV43'

# Create your views here.
def index(request):
    label = Label.objects.all()
    return render(request, 'index.html',{'label':label})

def about(request):
    return render(request, 'about.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid crentials')
            return redirect('login')
    else:
        return render(request, 'login.html')



def register(request):
    if request.method == 'POST':
       first_name = request.POST['first_name']
       last_name = request.POST['last_name']
       username = request.POST['username']
       password1 = request.POST['password1']
       password2 = request.POST['password2']
       email = request.POST['email']

       if password1 == password2:
           if User.objects.filter(username=username).exists():
               messages.info(request,'username Taken')
               return redirect('register')
           elif User.objects.filter(email=email).exists():
               messages.info(request,'Email Taken')
               return redirect('register')
           else:
               user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
               user.save();
               print('user created')
               return redirect('login')
       else:
           messages.info(request, 'password not matching')
           return redirect('register')

       return redirect('/')

    else:
        return render(request, 'register.html')



def booking(request,myid):
    if request.method == 'POST':
        car = request.POST.get('car', '')
        price = request.POST.get('price', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        pickup_location = request.POST.get('pickup_location', '')
        drop_location = request.POST.get('drop_location', '')
        pickup_date = request.POST.get('pickup_date', '')
        pickup_time = request.POST.get('pickup_time', '')
        special = request.POST.get('special', '')


        order = Order(first_name=first_name, last_name=last_name, email=email, phone=phone, pickup_location=pickup_location, drop_location=drop_location, pickup_date=pickup_date, pickup_time=pickup_time, special=special, car=car, price=price)
        order.save()


        param_dict = {
            'MID': 'pZYwlH74777163240584',
            'ORDER_ID': str(order.order),
            'TXN_AMOUNT': str(price),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})
    car = Cars.objects.filter(id=myid)
    return render(request, 'booking.html',{'car': car[0]})

@login_required(login_url='/login')
def car(request):
    cars_all = Cars.objects.all()
    paginator = Paginator(cars_all,6)
    page_number = request.GET.get('page')
    cars = paginator.get_page(page_number)
    return render(request, 'car.html',{'cars' : cars})

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email','')
        subject = request.POST.get('subject','')
        message = request.POST.get('message','')

        contact = Contact(name=name,email=email,subject=subject,message=message)
        contact.save()

    return render(request, 'contact.html')

def detail(request):
    return render(request, 'detail.html')

def service(request):
    return render(request, 'service.html')

def team(request):
    team = Team.objects.all()
    return render(request, 'team.html', {'team':team})

def testimonial(request):
    client = Testimonial.objects.all()
    return render(request, 'testimonial.html',{'client' : client})


def accinfo(request):
    user = request.user
    return render(request,'Accountinfo.html',{'user' :user})

def logout(request):
    auth.logout(request)
    return redirect('/')


def search(request):
    if request.method == "POST":
        search = request.POST['search']
        product = Cars.objects.filter(name__contains=search)
        return render(request, 'search.html', {'search':search,'product':product})
    else:
        return render(request, 'search.html')


def test(request):
    if request.method == 'POST':
        name = request.POST.get('first_name', '')

        order = Order(name=name)
        order.save()
    return render(request, 'test.html')

@csrf_exempt
def handlerequest(request):
    #paytm send request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order Successfull')
        else:
            print('order was not success full' + response_dict['RESPMSG'])
    return render(request,'paymentstatus.html',{'response': response_dict})