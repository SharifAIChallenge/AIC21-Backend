# Generated by Django 3.1.5 on 2021-03-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_team_level_one_payed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='teams/submissions'),
        ),
    ]
