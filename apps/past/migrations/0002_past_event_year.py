# Generated by Django 3.1.5 on 2021-02-25 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('past', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='past',
            name='event_year',
            field=models.CharField(default='-', max_length=128),
            preserve_default=False,
        ),
    ]
