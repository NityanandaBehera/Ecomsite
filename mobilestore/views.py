from cProfile import Profile
from django.shortcuts import render, redirect
from .models import*
import random
from django.core.paginator import Paginator
import http.client
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.core.mail import send_mail


def send_otp(mobile, otp):  # for otp i have used MSG91 api documents
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY  # you have add auth key in your setting.py
    headers = {'Content-Type': "application/json"}
    url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message=" + \
        "Your otp is "+otp + "&mobile="+mobile+"&authkey="+authkey+"&country=91"

    conn.request('GET', url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return None


def home(request):
    send_mail(
        'Testing mail',
        'welcome to us',
        'nityanandab306@gmail.com',
        ['nityanandabehera85132@gmail.com'],
        fail_silently=False,

    )
    return render(request, 'home.html')


def register(request):  # signup by getting email,name and phone no
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile=mobile).first()

        if check_user or check_profile:  # you have to check is there any user who have signup before using same email or phone no
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'signup.html', context)

        user = User(email=email, first_name=name)
        user.save()
        otp = str(random.randint(1000, 9999))  # creating 4 digit otp
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()
        send_otp(mobile, otp)  # calling send otp function
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request, 'signup.html')


def login(request):  # login using phone no
    if request.method != 'POST':
        return render(request, 'login.html')
    mobile = request.POST.get('mobile')

    user = Profile.objects.filter(mobile=mobile).first()

    if user is None:  # if you give wrong phone no it will show  user not found
        context = {'message': 'User not found', 'class': 'danger'}
        return render(request, 'login.html', context)

    otp = str(random.randint(1000, 9999))  # typecast the otp
    user.otp = otp
    user.save()
    send_otp(mobile, otp)
    request.session['mobile'] = mobile
    return redirect('otp')


def index(request):
    product_objects = Products.objects.all()
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:  # you can search here using phone title
        product_objects = product_objects.distinct().filter(
            Q(title__icontains=item_name) | Q(price__iexact=item_name))
    # pagination added in a single page there will be four no of phone will be displayed
    paginator = Paginator(product_objects, 4)
    page_number = request.GET.get('page')
    product_objects = paginator.get_page(page_number)

    return render(request, 'index.html', {'product_objects': product_objects})


def Details(request, id):  # you can view of a particular phone
    product_objects = Products.objects.get(id=id)
    print(product_objects)
    return render(request, 'detail.html', {'product_objects': product_objects})


def logout(request):  # you can logout yourself
    if request.method == 'POST':
        auth.logout(request)
        print('logged out from websites..')
        return redirect('home')


def otp(request):  # you can verify by using your otp.if you entered correct otp than go to index page otherwise wrong otp message will be appeared
    mobile = request.session['mobile']
    context = {'mobile': mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile=mobile).first()

        if otp == profile.otp:
            return redirect('index')
        context = {'message': 'Wrong OTP',
                   'class': 'danger', 'mobile': mobile}
        return render(request, 'otp.html', context)
    return render(request, 'otp.html', context)
# Create your views here.
