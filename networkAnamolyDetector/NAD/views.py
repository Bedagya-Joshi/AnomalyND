from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with your home page URL name
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to login page after successful logout
    return render(request, 'login.html')  # Display login form for GET requests

def home_view(request):
    return render(request, 'home.html')

def reports_view(request):
    return render(request, 'reports.html')

def notifications_view(request):
    return render(request, 'notifications.html')
