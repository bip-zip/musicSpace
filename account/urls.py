
from django.urls import path
from .views import SigninView, RegisterView
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    path('', SigninView.as_view(), name='signin'),
    path('register', RegisterView.as_view(), name='register'),
     path('logout', auth_views.LogoutView.as_view(), name='logout'),      
]
