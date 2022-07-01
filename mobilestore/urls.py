from django.urls import path
from .views import*
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name='home'),
    path('signup', register, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('index', index, name='index'),
    path('otp', otp, name='otp'),
    path('<int:id>/', Details, name="Details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
