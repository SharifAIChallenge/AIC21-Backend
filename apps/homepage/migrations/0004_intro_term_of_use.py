# Generated by Django 2.2.8 on 2019-12-27 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_auto_20191226_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='intro',
            name='term_of_use',
            field=models.TextField(null=True),
        ),
    ]
