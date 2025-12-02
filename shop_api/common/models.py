from django.db import models
from django.utils import timezone
# from venv import create
# from turtle import mode

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True