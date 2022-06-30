from cProfile import Profile
from django.shortcuts import render
from .models import*
import random


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile=mobile).first()
        if check_user or check_profile:
            context = {'message': 'user already exist', 'class': 'danger'}
            return render(request, 'signup.html', context)
        user = User(email=email, first_name=name)
        user.save()
        otp = str(random.randint(1000, 9999))
        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')


def otp(request):
    return render(request, 'otp.html')
# Create your views here.
