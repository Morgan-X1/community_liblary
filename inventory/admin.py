from django.contrib import admin
from .models import Category, Item

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')
    actions = ['approve_items']

    def approve_items(self, request, queryset):
        queryset.update(status='AVAILABLE')
    approve_items.short_description = "Approve selected items"
