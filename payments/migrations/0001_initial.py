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
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('gateway', models.CharField(choices=[('paypal', 'PayPal'), ('mp', 'MercadoPago')], max_length=10)),
                ('plan', models.CharField(choices=[('navegante', 'Plan Navegante'), ('practicante', 'Plan Practicante')], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('active', 'Activa'), ('paused', 'Pausada'), ('cancelled', 'Cancelada'), ('expired', 'Vencida')], default='pending', max_length=20)),
                ('gateway_subscription_id', models.CharField(blank=True, max_length=200)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('next_billing_date', models.DateField(blank=True, null=True)),
                ('cancelled_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='FractonesPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('gateway', models.CharField(max_length=10)),
                ('pack_slug', models.CharField(choices=[('pack_200', 'Explorador — 200 Fractones'), ('pack_500', 'Navegante+ — 500 Fractones'), ('pack_1200', 'Practicante+ — 1.200 Fractones')], max_length=20)),
                ('fractones', models.IntegerField()),
                ('amount_local', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
                ('gateway_payment_id', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('paid', 'Pagado'), ('failed', 'Fallido')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fractone_packs', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['gateway', 'gateway_subscription_id'], name='payments_su_gateway_idx'),
        ),
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['user', 'status'], name='payments_su_user_status_idx'),
        ),
        migrations.AddIndex(
            model_name='fractonespack',
            index=models.Index(fields=['gateway', 'gateway_payment_id'], name='payments_fp_gateway_idx'),
        ),
    ]
