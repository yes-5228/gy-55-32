from django.contrib import admin

from .models import ReturnOrder


@admin.register(ReturnOrder)
class ReturnOrderAdmin(admin.ModelAdmin):
    list_display = ("parcel", "reason", "operator", "status", "created_at", "completed_at")
    list_filter = ("reason", "status")
    search_fields = ("parcel__tracking_no", "operator")
