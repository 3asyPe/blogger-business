# Generated by Django 3.1 on 2020-10-18 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogger',
            old_name='name',
            new_name='blog_name',
        ),
    ]
