# Generated by Django 5.0.6 on 2024-06-19 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('braschüne', '0005_beer_is_crate'),
    ]

    operations = [
        migrations.AddField(
            model_name='beer',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
