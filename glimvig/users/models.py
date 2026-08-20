from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from pathlib import Path

User = get_user_model()

def profile_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f'profile_{instance.user.username}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{ext}'
    return Path('profile_photos') / str(instance.user.username) / new_filename


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    biography = models.TextField(blank=True, default="")
    photo = models.ImageField(upload_to=profile_photo_path, null=True, blank=True)

    def __str__(self): 
        return f'Profile of {self.user}'
