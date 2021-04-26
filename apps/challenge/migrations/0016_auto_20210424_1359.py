# Generated by Django 3.1.5 on 2021-04-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0015_mergescoreboards'),
    ]

    operations = [
        migrations.AddField(
            model_name='mergescoreboards',
            name='coef',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='mergescoreboards',
            name='cost',
            field=models.IntegerField(default=1000),
        ),
    ]