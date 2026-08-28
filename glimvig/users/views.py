from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.db.models import Avg 
from poems.models import Rating


User = get_user_model()

def profile(request, user_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    qs_user = User.objects.filter(pk=user_id).select_related('profile')
    profile_user = get_object_or_404(qs_user)

    user_poems = profile_user.poems.filter(is_published=True).all()

    count_of_poems = user_poems.count()

    qs_ratings = Rating.objects.filter(poem__authors=profile_user)
    total_ratings = qs_ratings.count()
    average_rating_of_all = qs_ratings.aggregate(
        average_of_all=Avg('value')
    )['average_of_all']

    context = {
        'profile_user': profile_user,
        'count_of_poems': count_of_poems,
        'total_ratings': total_ratings,
        'average_rating_of_all': average_rating_of_all,
        'user_poems': user_poems
    }

    return render(request, 'users/profile.html', context)

def favorites(request):
    return render(request, 'users/favorites.html')

def login(request):
    return render(request, 'users/login.html')

def register(request):
    return render(request, 'users/register.html')

def settings(request):
    return render(request, 'users/settings.html')