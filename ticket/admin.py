"""This file is used to register the models on admin site"""
from django.contrib import admin
from ticket.models import CustomUser


admin.site.register(CustomUser)
