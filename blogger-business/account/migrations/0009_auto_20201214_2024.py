# Generated by Django 3.1 on 2020-12-14 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]