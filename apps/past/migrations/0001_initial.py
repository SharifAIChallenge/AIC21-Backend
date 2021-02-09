from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Past',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('title_en', models.CharField(max_length=50)),
                ('title_fa', models.CharField(max_length=50)),
                ('description_en', models.TextField(max_length=300)),
                ('description_fa', models.TextField(max_length=300)),
                ('firstTeam' = models.TextField(max_length=50)),
                ('secondTeam' = models.TextField(max_length=50)),
                ('thirdTeam' = models.TextField(max_length=50)),
            ],
        ),
    ]