from django.contrib import admin
from .models import Category, Poem, Rating, FavoritePoem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'authors', 'text', 'teaser', 'categories', 'is_published',)
    readonly_fields = ('average_rating', 'updated_at', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    autocomplete_fields = ('poem',)

@admin.register(FavoritePoem)
class FavoritePoemAdmin(admin.ModelAdmin):
    pass


