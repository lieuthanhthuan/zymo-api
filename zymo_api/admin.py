from django.contrib import admin
from .models import Country, Region, CovidStats

# Register your models here.
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(CovidStats)
