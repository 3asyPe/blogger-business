# Generated by Django 3.1 on 2020-10-23 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201017_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(max_length=120),
        ),
    ]
