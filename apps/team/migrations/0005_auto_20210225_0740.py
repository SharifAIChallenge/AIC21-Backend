# Generated by Django 3.1.5 on 2021-02-25 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0004_auto_20210221_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='created_teams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('cpp', 'C++'), ('java', 'Java'), ('py3', 'Python 3')], default='java', max_length=50)),
                ('file', models.FileField(blank=True, null=True, upload_to='teams/None/submissions')),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
                ('is_final', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('uploading', 'Uploading'), ('uploaded', 'Uploaded'), ('compiling', 'Compiling'), ('compiled', 'Compiled'), ('failed', 'Failed')], default='uploading', max_length=50)),
                ('infra_compile_message', models.CharField(blank=True, max_length=1023, null=True)),
                ('infra_token', models.CharField(blank=True, max_length=256, null=True, unique=True)),
                ('infra_compile_token', models.CharField(blank=True, max_length=256, null=True, unique=True)),
                ('download_link', models.URLField(blank=True, max_length=512, null=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='team.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
