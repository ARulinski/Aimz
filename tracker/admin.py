from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Challenge, Profile

# Register your models here.

admin.site.register(Challenge)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile
    

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
