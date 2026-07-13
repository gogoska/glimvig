from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)

    context = {
        'profile_user': user,
    }

    return render(request, 'users\profile.html', context)

def favorites(request):
    return render(request, 'users/favorites.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html')

def settings(request):
    return render(request, 'users/settings.html')