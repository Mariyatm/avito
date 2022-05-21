from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class User(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    MEMBER = "member"
    ROLE = [(ADMIN, "Администратор"), (MODERATOR, "Модератор"), (MEMBER, "Участник")]

    role = models.CharField(max_length=30, choices=ROLE, default=MEMBER)
    age = models.IntegerField(null=True)
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    class Meta():
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'


