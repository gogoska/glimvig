from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rating, Poem

@receiver([post_save, post_delete], sender=Rating)
def update_poem_average_rating(sender, instance, **kwargs):
    poem = instance.poem
    avg = Rating.objects.filter(poem=poem).aggregate(Avg('value'))['value__avg']
    poem.average_rating = avg if avg is not None else 0
    poem.save(update_fields=['average_rating'])