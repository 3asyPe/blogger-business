# Generated by Django 3.1 on 2020-12-25 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0013_auto_20201214_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='offer_id',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]