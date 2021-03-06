# Generated by Django 3.1 on 2020-10-18 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blogger', '0003_auto_20201018_1458'),
        ('business', '0001_initial'),
        ('account', '0002_auto_20201017_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloggerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_group', models.CharField(choices=[('KIDS', 'Kids'), ('TEENAGERS', 'Teenagers'), ('ADULTS', 'Adults'), ('OLD', 'Old')], max_length=120)),
                ('sex', models.CharField(choices=[('M', 'MAN'), ('W', 'WOMAN')], max_length=1)),
                ('location', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.location')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('conditions', models.TextField()),
                ('price', models.IntegerField(blank=True, null=True)),
                ('barter', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('validity', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('DECLINED', 'DECLINED'), ('REQUESTED', 'REQUESTED')], max_length=255)),
                ('blogger_model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='offer.bloggermodel')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.business')),
            ],
        ),
        migrations.CreateModel(
            name='BloggersRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upvote', models.BooleanField()),
                ('blogger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogger.blogger')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.business')),
            ],
        ),
        migrations.CreateModel(
            name='BloggerModelSpecialization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(choices=[('TECH', 'Tech'), ('FUN CONTENT', 'Fun content'), ('BEAUTY', 'Beauty'), ('FASHION', 'Fashion')], max_length=100)),
                ('blogger_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.bloggermodel')),
            ],
        ),
        migrations.CreateModel(
            name='BloggerModelLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('EN', 'ENGLISH'), ('RU', 'RUSSIAN'), ('PL', 'POLISH')], max_length=2)),
                ('blogger_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.bloggermodel')),
            ],
        ),
    ]
