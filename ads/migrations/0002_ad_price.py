# Generated by Django 4.0.4 on 2022-04-21 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
