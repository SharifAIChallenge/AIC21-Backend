# Generated by Django 3.1.5 on 2021-03-09 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20210308_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='programming_language',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]