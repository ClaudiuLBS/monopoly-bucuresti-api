# Generated by Django 4.0.6 on 2022-08-05 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_gamerules'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gamerules',
            options={'verbose_name_plural': 'Game rules'},
        ),
        migrations.RenameField(
            model_name='gamerules',
            old_name='factory_output',
            new_name='factory_revenue',
        ),
    ]