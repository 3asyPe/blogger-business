# Generated by Django 3.1 on 2021-01-04 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0009_delete_youtubemanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubestatistics',
            name='month_views',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='youtubestatistics',
            name='total_views',
            field=models.BigIntegerField(default=0),
        ),
    ]