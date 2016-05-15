from django.contrib import admin
from core.models import Boby
from django.contrib.auth.admin import UserAdmin


class BobyAdmin(UserAdmin):
    pass

admin.site.register(Boby, BobyAdmin)
