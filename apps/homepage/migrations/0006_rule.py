# Generated by Django 3.1.5 on 2021-02-18 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_quote_sponsor_whythisevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_en', models.CharField(blank=True, max_length=50)),
                ('title_fa', models.CharField(max_length=50)),
                ('text_en', models.TextField(blank=True, max_length=10000)),
                ('text_fa', models.TextField(max_length=10000)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
    ]