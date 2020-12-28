# Generated by Django 3.1 on 2020-12-28 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0010_remove_blogger_youtube'),
        ('youtube', '0004_youtube_blogger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtube',
            name='blogger',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blogger.blogger'),
        ),
    ]
