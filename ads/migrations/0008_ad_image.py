# Generated by Django 4.0.4 on 2022-04-26 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0007_alter_ad_options_alter_cat_options_alter_ad_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
