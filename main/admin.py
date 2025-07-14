from django.contrib import admin
from .models import AppItem

@admin.register(AppItem)
class AppItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'apk_file')  # отображаем apk_file
    search_fields = ('title', 'description')
