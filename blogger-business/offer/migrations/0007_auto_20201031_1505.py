# Generated by Django 3.1 on 2020-10-31 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0006_auto_20201030_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloggermodel',
            name='age_group',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='bloggermodel',
            name='sex',
            field=models.CharField(max_length=3),
        ),
    ]
