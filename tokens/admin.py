from django.contrib import admin

from .models import Mission, MissionCompletion, TokenBalance, TokenTransaction


@admin.register(TokenBalance)
class TokenBalanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'permanent', 'monthly', 'balance']
    search_fields = ['user__email']
    readonly_fields = ['balance']


@admin.register(TokenTransaction)
class TokenTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'reason', 'created_at']
    list_filter = ['reason']
    search_fields = ['user__email']


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'fracton_reward', 'active', 'order']
    list_editable = ['active', 'order']


@admin.register(MissionCompletion)
class MissionCompletionAdmin(admin.ModelAdmin):
    list_display = ['user', 'mission', 'completed_at']
    search_fields = ['user__email']
