from django.views.generic import  CreateView
from django.contrib.auth.views import LoginView

from .forms import UserRegisterForm

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'account/register.html'
    success_url = '/auth'


class SigninView(LoginView):
    template_name='account/login.html'
    success_message = "You were successfully logged in."