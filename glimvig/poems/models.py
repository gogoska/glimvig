from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from datetime import datetime
from pathlib import Path

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self): 
        return f'Category "{self.name}"'


class Poem(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заговок')
    text = models.TextField(verbose_name='Текст')
    teaser = models.CharField(max_length=500, blank=True, default='', verbose_name='Тизер')
    authors = models.ManyToManyField(User, related_name='poems', verbose_name='Авторы')
    average_rating = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name='Рейтинг')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name='Время редактирования')
    is_published = models.BooleanField(default=False, verbose_name='Публикация')
    categories = models.ManyToManyField(Category, related_name='poems', verbose_name='Категории')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self): 
        return f'Poem "{self.title}"'

class PoemConnection(models.Model):
    from_poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='poem_connections_from')
    to_poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='poem_connections_to')
    description = models.TextField()

    def __str__(self): 
        return f'Connection "{self.from_poem.title}" ---> "{self.to_poem.title}"'


def poem_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f'poem_{instance.poem.slug}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{ext}'
    return Path('poem_photos') / str(instance.poem.slug) / new_filename


class PoemPhoto(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='poem_photos') # Poem
    img = models.ImageField(upload_to=poem_photo_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self): 
        return f'Photo for "{self.poem.title}"'

class Comment(models.Model):
    text = models.CharField(max_length=500)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_published = models.BooleanField(default=False)

    def __str__(self): 
        return f'Comment {self.user} ---> {self.poem}'

class FavoritePoem(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='favorite_poems')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_poems')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self): 
        return f'Favorite poem {self.user} ---> "{self.poem}"'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'poem'], name='unique_favorite_poem')
        ]


class Rating(models.Model):
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='ratings') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self): 
        return f'Rating {self.user} ---> "{self.poem}" is {str(self.value)}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'poem'], name='unique_rating')
        ]