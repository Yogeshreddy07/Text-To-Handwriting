from django.contrib import admin
from .models import News



@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Display title and creation date in the admin list view
    search_fields = ('title',)  # Add a search bar for titles
