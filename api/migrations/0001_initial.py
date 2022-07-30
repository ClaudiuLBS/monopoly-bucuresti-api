# Generated by Django 4.0.6 on 2022-07-30 14:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(default=datetime.datetime(2022, 7, 30, 14, 34, 42, 458078))),
                ('code', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='NeighbourHood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=9)),
                ('price', models.IntegerField(default=0)),
                ('rent', models.IntegerField(default=0)),
                ('house_price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('money', models.IntegerField(default=1500)),
                ('owner', models.BooleanField(default=False)),
                ('game_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.gamesession')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('houses', models.IntegerField(default=0)),
                ('neighbourHood', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.neighbourhood')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.player')),
            ],
        ),
    ]
