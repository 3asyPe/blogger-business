# Generated by Django 3.1 on 2020-10-18 14:29

import blogger.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0003_auto_20201018_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogger',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=blogger.models.upload_image_path_blogger),
        ),
    ]