"""Django admin for user login and sign up functionality"""
# from django.contrib import admin # pylint: disable=unused-import
from django.contrib import admin
from .models import Notification
# Register your models here.
admin.site.register(Notification)
