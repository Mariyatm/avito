from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.CharField(max_length=1500)
    address = models.CharField(max_length=50)
    is_published = models.BooleanField()


class Cat(models.Model):
    name = models.CharField(max_length=50)
