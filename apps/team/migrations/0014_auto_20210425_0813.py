# Generated by Django 3.1.5 on 2021-04-25 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0013_auto_20210411_0730'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='final_payed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='is_finalist',
            field=models.BooleanField(default=False),
        ),
    ]