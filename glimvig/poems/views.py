from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse, Http404
from django_htmx.http import HttpResponseClientRedirect
from django.urls import reverse
from django.db.models import Count, OuterRef, Exists, Prefetch, Value, BooleanField, Subquery, IntegerField
from django.contrib.auth import get_user_model
from .models import Poem, FavoritePoem, Rating
from .forms import RatingForm

User = get_user_model()

def toggle_favorite(request, poem_slug):
    if not request.headers.get('HX-Request'):
        return Http404()
    if not request.user.is_authenticated:
        return HttpResponseClientRedirect(reverse('users:login'))

    poem = get_object_or_404(Poem, slug=poem_slug)
    user = request.user

    favorite_poem_record, created = FavoritePoem.objects.get_or_create(
        user_id=user.id, 
        poem_id=poem.id
    )
    if not created:
        favorite_poem_record.delete()

    context = {
        'poem_slug': poem_slug,
        'is_favorite': created,
    }

    return render(request, 'poems/_toggle_favorite_button.html', context)

def home(request):
    if request.headers.get('HX-Request'):
        if not request.user.is_authenticated:
            return HttpResponseClientRedirect(reverse('users:login'))
        if request.method == 'GET':
            return HttpResponse('Действие пока не реализовано', status=501)
        elif request.method == 'POST':
            return HttpResponse('Действие пока не реализовано', status=501)
        else:
            return HttpResponseNotAllowed(['GET', 'POST'])

    poems = Poem.objects.filter(is_published=True).annotate(
        votes_count=Count('ratings')
    ).prefetch_related(
        Prefetch('authors', queryset=User.objects.only('id', 'username'))
    )

    user = request.user
    if user.is_authenticated:
        favorite_poems_subquery = FavoritePoem.objects.filter(
            user=user,
            poem=OuterRef('pk'),
        )

        poems = poems.annotate(
            is_favorite=Exists(favorite_poems_subquery),
        )
    else:
        poems = poems.annotate(
            is_favorite=Value(False, output_field=BooleanField()),
        )

    context = {
        'poems': poems,
    }

    return render(request, 'poems/home.html', context)

def set_rating(request, poem_slug):
    if not request.headers.get('HX-Request'):
        return Http404()
    if not request.user.is_authenticated:
        return HttpResponseClientRedirect(reverse('users:login'))

    poem = get_object_or_404(Poem, slug=poem_slug)
    user = request.user

    poem_rating_form = RatingForm(request.POST)
    if poem_rating_form.is_valid():
        value = poem_rating_form.cleaned_data['value']

        rating, created = Rating.objects.get_or_create(
            user=user,
            poem=poem,
            defaults={'value': value}
        )

        if not created:
            rating.value = value
            rating.save()

        poem_rating_form = RatingForm(instance=rating)

    poem = get_object_or_404(Poem, slug=poem_slug)

    user_rating_obj = poem.ratings.filter(user=user).first()
    poem_user_rating = user_rating_obj.value if user_rating_obj else None
    poem_average_rating = poem.average_rating
    poem_votes_count = poem.ratings.count()

    context = {
        'poem_user_rating': poem_user_rating,
        'poem_average_rating': poem_average_rating,
        'poem_votes_count': poem_votes_count,
        'poem_slug': poem_slug,
        'poem_rating_form': poem_rating_form,
    }

    response_html = render_to_string('poems/_poem_rating_label.html', context, request)
    
    stats_html = render_to_string('poems/_poem_rating_form.html', context, request)

    return HttpResponse(response_html + stats_html)
    

def poem_detail(request, poem_slug):
    qs = Poem.objects.filter(is_published=True, slug=poem_slug).annotate(
        votes_count=Count('ratings')
    ).prefetch_related(
        Prefetch('authors', queryset=User.objects.only('id', 'username'))
    )

    user = request.user
    if user.is_authenticated:
        favorite_poems_subquery = FavoritePoem.objects.filter(
            user=user,
            poem=OuterRef('pk'),
        )

        user_rating_subquery = Rating.objects.filter(
            user=user,
            poem=OuterRef('pk'),
        ).values('value')[:1]

        qs = qs.annotate(
            is_favorite=Exists(favorite_poems_subquery),
            user_rating=Subquery(user_rating_subquery, output_field=IntegerField()),
        )

    poem = get_object_or_404(qs)

    rating = None
    if user.is_authenticated:
        rating = Rating.objects.filter(user=user, poem=poem).first()

    if rating:
        poem_rating_form = RatingForm(instance=rating)
    else:
        poem_rating_form = RatingForm()

    context = {
        'poem': poem,
        'poem_rating_form': poem_rating_form,      
    }

    return render(request, 'poems/poem_detail.html', context)

def about(request):
    return render(request, 'poems/about.html')

def poem_create(request):
    return render(request, 'poems/poem_create.html')

def poem_edit(request):
    return render(request, 'poems/poem_edit.html')

def profile_graph(request):
    return render(request, 'poems/profile_graph.html')

def search(request):
    return render(request, 'poems/search.html')