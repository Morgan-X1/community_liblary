from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('item__name', 'user__username')
    actions = ['mark_as_active', 'mark_as_completed', 'mark_as_cancelled']

    def mark_as_active(self, request, queryset):
        queryset.update(status='ACTIVE')
        # Logic to update item status to ON_LOAN could be added here or via signals
    mark_as_active.short_description = "Mark selected reservations as Active"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='COMPLETED')
    mark_as_completed.short_description = "Mark selected reservations as Completed"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
    mark_as_cancelled.short_description = "Mark selected reservations as Cancelled"
