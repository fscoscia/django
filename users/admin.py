from django.contrib import admin

from users.models import UserProfile

from django.contrib.auth.admin import UserAdmin

admin.site.register(UserProfile)
