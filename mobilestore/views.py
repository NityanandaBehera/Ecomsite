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


def send_otp(mobile, otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = {'Content-Type': "application/json"}
    url = f"http://control.msg91.com/api/sendotp.php?otp={otp}&message=Your otp is {otp}&mobile={mobile}&authkey=" + {
        authkey} + "&country=91"

    conn.request('GET', url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return None


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile=mobile).first()

        if check_user or check_profile:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'signup.html', context)

        user = User(email=email, first_name=name)
        user.save()
        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request, 'signup.html')


def login(request):
    if request.method != 'POST':
        return render(request, 'login.html')
    mobile = request.POST.get('mobile')

    user = Profile.objects.filter(mobile=mobile).first()

    if user is None:
        context = {'message': 'User not found', 'class': 'danger'}
        return render(request, 'login.html', context)

    otp = str(random.randint(1000, 9999))
    user.otp = otp
    user.save()
    send_otp(mobile, otp)
    request.session['mobile'] = mobile
    return redirect('otp')


def index(request):
    product_objects = Products.objects.all()
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.distinct().filter(
            Q(title__icontains=item_name) | Q(price__iexact=item_name))
    paginator = Paginator(product_objects, 4)
    page_number = request.GET.get('page')
    product_objects = paginator.get_page(page_number)

    return render(request, 'index.html', {'product_objects': product_objects})


def Details(request, id):
    product_objects = Products.objects.get(id=id)
    print(product_objects)
    return render(request, 'detail.html', {'product_objects': product_objects})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        print('logged out from websites..')
        return redirect('home')


def otp(request):
    mobile = request.session['mobile']
    context = {
        'mobile': mobile
    }
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
