# Generated by Django 4.0.4 on 2022-04-26 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0009_alter_ad_options_remove_ad_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='description',
            field=models.CharField(max_length=1500, null=True),
        ),
    ]
