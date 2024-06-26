# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Login Successful!"))
            return redirect('index')
            
        else:
            messages.success(request, ("Incorrect Credentilas, Try again!"))
            return redirect('login_user')
        
    return render(request, "members/login.html")

def logout_user(request):
    logout(request)
    return redirect('index')

def register_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Registration Successful! Please Login"))
            return redirect('login_user')

    context = {'form': form}
    
    return render(request, "members/register.html", context)

def profile_user(request):
    return render(request, "members/profile.html")
