from django.contrib import admin
from .models import Poem

@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

