# Generated by Django 3.1.5 on 2021-02-25 07:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('team', '0004_auto_20210221_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('file', models.FileField(upload_to='maps/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(choices=[('failed', 'Failed'), ('successful', 'Successful'), ('running', 'Running')], default='running', max_length=50)),
                ('log', models.FileField(blank=True, null=True, upload_to='match/logs/')),
                ('is_freeze', models.BooleanField(default=True)),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_first', to='team.team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_second', to='team.team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Scoreboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('freeze', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=512)),
                ('types', models.CharField(choices=[('successful', 'Normal'), ('friendly', 'Friendly'), ('clanwar', 'Clanwar')], default='successful', max_length=50)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_hidden', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScoreboardRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('score', models.PositiveIntegerField(default=0)),
                ('wins', models.PositiveIntegerField(default=0)),
                ('losses', models.PositiveIntegerField(default=0)),
                ('draws', models.PositiveIntegerField(default=0)),
                ('scoreboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='challenge.scoreboard')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='scoreboard_rows', to='team.team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='scoreboard',
            name='tournament',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='scoreboard', to='challenge.tournament'),
        ),
        migrations.CreateModel(
            name='MatchInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('team1_score', models.PositiveIntegerField()),
                ('team2_score', models.PositiveIntegerField()),
                ('match_duration', models.DurationField()),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_info', to='challenge.map')),
                ('match', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='match_info', to='challenge.match')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='challenge.tournament'),
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='won_matches', to='team.team'),
        ),
    ]
