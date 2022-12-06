from django.contrib import admin

from .models import Thread, ChatMessage, Inbox


class ChatMessageInlineAdmin(admin.TabularInline):
    model = ChatMessage


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "thread",
        "user",
        "receiver",
        "message",
        "timestamp",
        "message_type",
        "media_item",
        "purchase_cost_currency",
        "purchase_cost_amount",
    )


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessageInlineAdmin]
    list_display = ('first', 'second', 'id', 'timestamp', 'updated')
    readonly_fields = ('updated', 'timestamp')

    class Meta:
        model = Thread


class InboxAdmin(admin.ModelAdmin):
    list_display = ('user', 'second', 'id', 'timestamp', 'updated')
    fieldsets = (
        (None, {'fields': ('user', 'second', 'last_message', 'read')}),

    )
    readonly_fields = ('updated', 'timestamp')

    class Meta:
        model = Inbox


admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Inbox, InboxAdmin)