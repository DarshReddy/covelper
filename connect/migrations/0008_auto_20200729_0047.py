# Generated by Django 3.0.8 on 2020-07-28 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0007_auto_20200729_0040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='hw_id',
            new_name='hworker',
        ),
        migrations.RenameField(
            model_name='request',
            old_name='p_id',
            new_name='patient',
        ),
    ]