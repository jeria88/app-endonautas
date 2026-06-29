from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_kpisnapshot_facebook_seguidores'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpisnapshot',
            name='linkedin_seguidores',
            field=models.IntegerField(default=0),
        ),
    ]
