from django.contrib import admin

from .models import Question, Test, TestResult


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ['text', 'dimension_key', 'scale', 'reverse_scored', 'order']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['name', 'dimension', 'instrument_type', 'active', 'order']
    list_filter = ['dimension', 'instrument_type', 'active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [QuestionInline]


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'completed_at']
    list_filter = ['test']
    search_fields = ['user__email']
    readonly_fields = ['raw_scores', 'evaluation', 'ai_insight']
