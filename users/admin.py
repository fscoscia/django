from django.contrib import admin

from users.models import UserProfile

from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.StackedInline):
    model = UserProfile


UserAdmin.inlines = [ProfileInline]
