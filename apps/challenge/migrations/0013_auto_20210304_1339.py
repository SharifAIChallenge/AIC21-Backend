# Generated by Django 3.1.5 on 2021-03-04 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0005_auto_20210225_0740'),
        ('challenge', '0012_auto_20210304_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clanteam',
            name='team',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='clan_team', to='team.team'),
        ),
    ]
