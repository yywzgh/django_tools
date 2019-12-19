from django.db import models
from django.contrib import admin


class UserInfo(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)