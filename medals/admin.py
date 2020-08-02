from django.contrib import admin
from .models import Medals


class MedalsAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Medals, MedalsAdmin)
