from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_kpisnapshot_tiktok_seguidores'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpisnapshot',
            name='youtube_seguidores',
            field=models.IntegerField(default=0),
        ),
    ]
