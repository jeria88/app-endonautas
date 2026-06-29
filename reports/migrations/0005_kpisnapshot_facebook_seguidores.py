from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_kpisnapshot_youtube_seguidores'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpisnapshot',
            name='facebook_seguidores',
            field=models.IntegerField(default=0),
        ),
    ]
