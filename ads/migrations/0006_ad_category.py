# Generated by Django 4.0.4 on 2022-04-25 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_alter_ad_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ads.cat'),
        ),
    ]
