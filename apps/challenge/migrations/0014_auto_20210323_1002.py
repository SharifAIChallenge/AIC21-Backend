# Generated by Django 3.1.5 on 2021-03-23 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0013_auto_20210318_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lobbyqueue',
            name='game_type',
            field=models.CharField(choices=[('friendly_match', 'Friendly match'), ('level_based_tournament', 'Level based tournament')], max_length=50),
        ),
    ]
