# Generated by Django 4.0.4 on 2022-04-26 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0008_ad_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ad',
            options={'verbose_name': 'Объявление', 'verbose_name_plural': 'Объявления'},
        ),
        migrations.RemoveField(
            model_name='ad',
            name='address',
        ),
    ]