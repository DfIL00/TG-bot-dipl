from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'last_activity')
    search_fields = ('username', 'email')


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'started_at', 'is_active')
    list_filter = ('is_active',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'text', 'is_bot', 'timestamp')
    readonly_fields = ('timestamp',)


@admin.register(BotResponseTemplate)
class BotResponseTemplateAdmin(admin.ModelAdmin):
    list_display = ('trigger_word', 'priority', 'response_text')
    ordering = ('-priority',)


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')

BotResponseTemplate.objects.create(
    trigger_word="погода",
    response_text="Прогноз: солнечно, +25°C",
    priority=1
)


# Register your models here.
