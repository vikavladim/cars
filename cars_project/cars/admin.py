from django.contrib import admin
from .models import Car, Comment


class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'make', 'model', 'year', 'description', 'created_at', 'updated_at', 'owner')
    list_filter = ('make', 'model', 'year', 'created_at', 'updated_at', 'owner')
    search_fields = ('make', 'model', 'description', 'owner__username')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'created_at', 'car', 'author')
    list_filter = ('created_at', 'car', 'author')
    search_fields = ('content', 'car__make', 'car__model', 'author__username')

admin.site.register(Car, CarAdmin)
admin.site.register(Comment, CommentAdmin)