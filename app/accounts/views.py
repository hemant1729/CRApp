from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

#username: admin, password: 12345
#username: temp, password: 1234


def is_admin(request):
    return request.user.username=='admin'
    

def home(request):
    if request.user.is_authenticated:
        if is_admin(request):
            return redirect('admin/')
        else:
            return redirect('student/')
    else:
        return redirect('login/')


def login_view(request):
    error = ""
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        print(username, password)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error = "Invalid credentials"
    context = {'error': error}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def register(request):
    error = ""
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        print(username, password)

        try:
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()
        except:
            error = "Invalid form data or user already exists"
            context = {'error': error}
            return render(request, 'accounts/registration.html', context)
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    context = {'error': error}
    return render(request, 'accounts/registration.html', context)