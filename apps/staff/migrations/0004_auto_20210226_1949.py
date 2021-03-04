# Generated by Django 3.1.5 on 2021-02-26 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_staff_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='first_name_en',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='last_name_en',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
