from users.forms import LoginForm,PasswordChangeForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from . models import User

# Create your views here.

def index(request):
    
    
    return render(request, 'users/index.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('hr:dashboard'))
            else:
                return render(request,"users/login.html",{
                    "form": form
                })
        else:
             return render(request,"users/login.html",{
                    "form": form
                })
    form = LoginForm()
    return render(request,"users/login.html",{
                    "form": form
                })

def password_change_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            user = User.objects.get(username=request.user.username)
            user.set_password(password1)
            user.save()
        else:
             return render(request,"users/password_change.html",{
                    "form": form
                })
    form = PasswordChangeForm()
    return render(request,"users/password_change.html",{
                    "form": form
                })

def logout_view(request):
    
    logout(request)
    return render(request, 'users/logout.html')