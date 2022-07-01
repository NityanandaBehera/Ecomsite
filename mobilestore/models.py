from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField
from ckeditor.fields import RichTextField
from colorfield.fields import ColorField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
# Create your models here.


class Products(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField()
    category = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='uploads')
    color = ColorField(image_field='image')

    class Meta:
        ordering = ['price']
