from django.core.validators import RegexValidator
from django.db import models


class SignUpModel(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=60)
    password = models.CharField(max_length=16)


class SignInModel(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=16)
