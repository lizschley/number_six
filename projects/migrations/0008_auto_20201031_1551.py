# Generated by Django 3.0.7 on 2020-10-31 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20201031_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='cat_sort',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
