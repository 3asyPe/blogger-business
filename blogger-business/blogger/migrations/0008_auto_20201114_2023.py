# Generated by Django 3.1 on 2020-11-14 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0007_blogger_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglanguage',
            name='blogger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='blogger.blogger'),
        ),
        migrations.AlterField(
            model_name='blogspecialization',
            name='blogger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specializations', to='blogger.blogger'),
        ),
    ]
