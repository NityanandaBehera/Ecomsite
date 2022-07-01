from cProfile import Profile
from django.contrib import admin
from .models import*
admin.site.register(Profile)
admin.site.register(Products)

# Register your models here.
