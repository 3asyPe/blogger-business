# Generated by Django 3.1 on 2020-11-01 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0010_remove_bloggermodel_subscribers_number_group'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BloggersRate',
        ),
    ]