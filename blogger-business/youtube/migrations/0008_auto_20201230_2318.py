# Generated by Django 3.1 on 2020-12-30 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0007_auto_20201230_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribers', models.IntegerField(default=0)),
                ('total_video_count', models.IntegerField(default=0)),
                ('total_views', models.IntegerField(default=0)),
                ('total_updated', models.DateTimeField(blank=True, null=True)),
                ('month_views', models.IntegerField(default=0)),
                ('month_comments', models.IntegerField(default=0)),
                ('month_subscribers_gained', models.IntegerField(default=0)),
                ('month_likes', models.IntegerField(default=0)),
                ('month_dislikes', models.IntegerField(default=0)),
                ('month_updated', models.IntegerField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('youtube', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='youtube.youtube')),
            ],
        ),
        migrations.DeleteModel(
            name='YoutubeMonthStatistics',
        ),
    ]