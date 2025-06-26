from django.contrib import admin

# Register your models here.
from django.db import models

class CCode(models.Model):
    code = models.TextField()

    def __str__(self):
        return self.code