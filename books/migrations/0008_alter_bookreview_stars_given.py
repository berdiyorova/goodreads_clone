# Generated by Django 4.0 on 2024-02-28 10:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_alter_bookreview_stars_given'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='stars_given',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
