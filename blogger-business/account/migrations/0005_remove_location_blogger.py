# Generated by Django 3.1 on 2020-10-27 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_location_blogger'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='blogger',
        ),
    ]
