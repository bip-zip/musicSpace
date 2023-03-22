
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('musicmaker.urls')),
    path('auth/',include('account.urls')),
    
]
