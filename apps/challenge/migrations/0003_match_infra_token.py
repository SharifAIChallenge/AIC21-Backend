# Generated by Django 3.1.5 on 2021-03-28 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0002_map_infra_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='infra_token',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
