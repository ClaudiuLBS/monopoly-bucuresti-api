# Generated by Django 4.0.6 on 2022-07-30 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_gamesession_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
