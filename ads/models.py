# from django.contrib.auth.models import User
from django.db import models
from users.models import User


class Cat(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Ad(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.IntegerField()
    description = models.CharField(max_length=1500, null=True)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='images/', null=True)
    category = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    @property
    def username(self):
        return self.user.username if self.user else None
