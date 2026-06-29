from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_kpisnapshot_linkedin_seguidores'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpisnapshot',
            name='top_content',
            field=models.JSONField(default=dict),
        ),
    ]
