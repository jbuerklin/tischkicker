# Generated by Django 5.0.6 on 2024-06-19 09:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('braschüne', '0007_twoplayersgame'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ThreePlayersGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_round', models.SmallIntegerField(default=-1)),
                ('round_name', models.CharField(default='', max_length=64)),
                ('finished', models.BooleanField(default=False)),
                ('ev_defensive', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='three_ev_defensive', to=settings.AUTH_USER_MODEL)),
                ('ev_offensive', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='three_ev_offensive', to=settings.AUTH_USER_MODEL)),
                ('sd_player', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='three_sd_player', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
