from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=20)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

class User(models.Model):
    ROLE = [("admin", "Администратор"), ("moderator", "Модератор"), ("member", "Участник")]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLE, default="member")
    age = models.IntegerField(null=True)
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    class Meta():
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'


