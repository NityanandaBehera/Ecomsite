from django.urls import path
from .views import*
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name='home'),
    path('signup', register, name='signup'),
    path('login', login, name='login'),
    path('index', index, name='index'),
    path('otp', otp, name='otp'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
