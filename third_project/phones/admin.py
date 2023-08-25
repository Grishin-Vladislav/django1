from django.contrib import admin
from .models import Phone


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'lte_exists', 'release_date']
    list_filter = ['lte_exists', 'price']
