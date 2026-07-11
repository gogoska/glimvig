from django.shortcuts import render

def profile(request):
    return render(request, 'users\profile.html')

def favorites(request):
    return render(request, 'users/favorites.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html')

def settings(request):
    return render(request, 'users/settings.html')