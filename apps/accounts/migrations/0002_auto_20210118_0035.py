# Generated by Django 3.1.5 on 2021-01-17 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivateUserToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('eid', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='province',
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname_fa', models.TextField(max_length=30)),
                ('firstname_en', models.TextField(max_length=30)),
                ('lastname_fa', models.TextField(max_length=30)),
                ('lastname_en', models.TextField(max_length=30)),
                ('university', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=128)),
                ('major', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
