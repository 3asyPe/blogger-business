# Generated by Django 3.1 on 2020-12-20 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_remove_emailactivation_expires'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailactivation',
            name='email_change',
            field=models.BooleanField(default=False),
        ),
    ]