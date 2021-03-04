# Generated by Django 3.1.5 on 2021-03-04 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0005_auto_20210225_0740'),
        ('challenge', '0011_auto_20210225_1650'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clanteam',
            name='teams',
        ),
        migrations.AddField(
            model_name='clanteam',
            name='team',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.RESTRICT, related_name='clan', to='team.team'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clanteam',
            name='clan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='challenge.clan'),
        ),
    ]
