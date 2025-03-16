from django.contrib import admin

from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'available') 
    search_fields = ('make', 'model') 
