# Generated by Django 4.0 on 2024-02-27 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_bookreview_stars_given'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='stars_given',
            field=models.IntegerField(default=0),
        ),
    ]
