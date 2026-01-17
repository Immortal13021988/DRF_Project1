from django.contrib import admin

from .models import User


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    exclude = ("password",)
# Register your models here.
