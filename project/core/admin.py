from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Boby


class BobyAdmin(UserAdmin):
    pass

admin.site.register(Boby, BobyAdmin)
