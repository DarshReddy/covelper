# Generated by Django 3.0.8 on 2020-07-19 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0002_auto_20200718_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='req_at',
            field=models.TimeField(auto_now=True),
        ),
    ]