# Generated by Django 3.0.7 on 2020-08-12 18:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20200811_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
