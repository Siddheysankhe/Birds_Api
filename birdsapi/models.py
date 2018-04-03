from __future__ import unicode_literals

from django.db import models

# Create your models here.


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Bird_Info(models.Model):
    common_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    image = models.FileField(blank=False,null=False)
    audio = models.FileField(blank=False,null=False)
    description = models.CharField(max_length=1000)
    habitat = models.CharField(max_length=100)
    location = models.CharField(max_length=100)