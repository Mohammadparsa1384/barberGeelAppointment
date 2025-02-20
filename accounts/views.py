from django.shortcuts import redirect, render
from django.urls import  reverse_lazy
from .forms import CustomUserCreationForm
from django.views import generic
from django.contrib import messages
from django.contrib.auth.views import LoginView

# Create your views here.
class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    
    def form_valid(self, form):
        messages.success(self.request, "ثبت‌ نام شما با موفقیت انجام شد! اکنون می‌توانید وارد شوید.")
        return super().form_valid(form)
    