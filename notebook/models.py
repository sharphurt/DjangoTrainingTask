from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=CASCADE, default='admin')
