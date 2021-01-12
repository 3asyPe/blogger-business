# Generated by Django 3.1 on 2021-01-11 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0020_auto_20210111_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloggermodel',
            name='offer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blogger_model', to='offer.offer'),
        ),
    ]
