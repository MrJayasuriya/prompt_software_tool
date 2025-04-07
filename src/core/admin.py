from django.contrib import admin
from .models import Chat

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user_input', 'response', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user_input', 'response', 'prompt_used', 'system_message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Input & Response', {
            'fields': ('user_input', 'response')
        }),
        ('Prompt Settings', {
            'fields': ('prompt_used', 'system_message'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        # Disable adding chats through admin
        return False
