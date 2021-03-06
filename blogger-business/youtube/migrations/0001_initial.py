# Generated by Django 3.1 on 2020-12-28 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Youtube',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('image_url', models.URLField(blank=True, null=True)),
                ('access_token', models.CharField(max_length=255)),
                ('updated_token', models.DateField()),
                ('token_expires_in', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeMonthStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField()),
                ('dislikes', models.IntegerField()),
                ('comments', models.IntegerField()),
                ('subscribers_gained', models.IntegerField()),
                ('views', models.IntegerField()),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('youtube', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='youtube.youtube')),
            ],
        ),
    ]
