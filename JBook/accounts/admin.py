from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

User = get_user_model()

class MyCustomUserInline(admin.StackedInline):
    model = models.UserProfile
    can_delete = True
    verbose_name = 'Profile'

class MyUserAdmin(BaseUserAdmin):
    inlines = (MyCustomUserInline, )
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
