# Generated by Django 3.0.8 on 2020-07-19 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0003_request_req_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='req_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]