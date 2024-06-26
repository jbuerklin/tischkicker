# Generated by Django 5.0.6 on 2024-06-18 06:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('braschüne', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='fourplayersgame',
            name='ev_defensive',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_defensive', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fourplayersgame',
            name='ev_offensive',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ev_offensive', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fourplayersgame',
            name='sd_defensive',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sd_defensive', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fourplayersgame',
            name='sd_offensive',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sd_offensive', to=settings.AUTH_USER_MODEL),
        ),
    ]
