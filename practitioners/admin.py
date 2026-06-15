from django.contrib import admin

from .models import Availability, SessionNote, TemporaryProfile, TherapySession


@admin.register(TemporaryProfile)
class TemporaryProfileAdmin(admin.ModelAdmin):
    list_display = ['alias', 'practitioner', 'claimed_by', 'email', 'created_at']
    search_fields = ['alias', 'practitioner__email', 'email']
    readonly_fields = ['access_code']


@admin.register(SessionNote)
class SessionNoteAdmin(admin.ModelAdmin):
    list_display = ['profile', 'practitioner', 'session_date', 'created_at']
    list_filter = ['session_date']


@admin.register(TherapySession)
class TherapySessionAdmin(admin.ModelAdmin):
    list_display = ['profile', 'practitioner', 'datetime', 'session_type', 'status']
    list_filter = ['status', 'session_type']


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['practitioner', 'day_of_week', 'start_time', 'end_time', 'active']
    list_filter = ['day_of_week', 'active']
