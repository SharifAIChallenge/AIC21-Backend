# Generated by Django 3.1.5 on 2021-04-05 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0016_auto_20210405_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='title',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]
