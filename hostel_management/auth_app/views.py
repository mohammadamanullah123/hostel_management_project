from django.shortcuts import render

# Create your views here.
# auth_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from hostel_app.models import Student

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        roll_no = request.POST['roll_no']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Student.objects.create(user=user, name=name, email=email, roll_no=roll_no)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    
    return render(request, 'auth/register.html')