# Generated by Django 3.1.5 on 2021-03-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20210316_1144'),
    ]

    operations = [
        migrations.CreateModel(
            name='MajorAPIConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=256)),
                ('headers', models.TextField()),
            ],
        ),
    ]