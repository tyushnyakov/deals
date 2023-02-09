from django.db import models


class Deal(models.Model):
    customer = models.CharField(max_length=20)
    item = models.CharField(max_length=20)
    total = models.PositiveSmallIntegerField()
    quantity = models.PositiveSmallIntegerField()
    date = models.DateTimeField()
