from django.contrib import admin

from .models import FractonesPack, Subscription, TallerReserva


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'gateway', 'status', 'started_at', 'created_at')
    list_filter = ('gateway', 'plan', 'status')
    search_fields = ('user__email', 'gateway_subscription_id')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(FractonesPack)
class FractonesPackAdmin(admin.ModelAdmin):
    list_display = ('user', 'pack_slug', 'fractones', 'gateway', 'status', 'currency', 'amount_local', 'created_at')
    list_filter = ('gateway', 'pack_slug', 'status')
    search_fields = ('user__email', 'gateway_payment_id')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TallerReserva)
class TallerReservaAdmin(admin.ModelAdmin):
    list_display = ('user', 'taller_slug', 'gateway', 'status', 'currency', 'amount_local', 'created_at')
    list_filter = ('gateway', 'taller_slug', 'status')
    search_fields = ('user__email', 'gateway_payment_id')
    readonly_fields = ('created_at', 'updated_at')
