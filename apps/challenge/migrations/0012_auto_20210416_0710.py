# Generated by Django 3.1.5 on 2021-04-16 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0011_league_total_matches'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='run',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]