from django.db import models

# Create your models here.

class HeartBeatValue(models.Model):
    HB = models.FloatField(null=True)
