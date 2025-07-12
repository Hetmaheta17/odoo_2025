from django.contrib import admin
from .models import User, Item, Tag

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'status', 'approved', 'created_at')
    list_filter = ('approved', 'status', 'category')
    actions = ['approve_items']

    def approve_items(self, request, queryset):
        queryset.update(approved=True)
    approve_items.short_description = "Mark selected items as approved"

admin.site.register(User)
admin.site.register(Item, ItemAdmin)
admin.site.register(Tag)