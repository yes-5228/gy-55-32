from django.contrib import admin

from .models import LockerCell


@admin.register(LockerCell)
class LockerCellAdmin(admin.ModelAdmin):
    list_display = ("code", "zone", "size", "status", "temperature", "updated_at")
    list_filter = ("zone", "size", "status")
    search_fields = ("code",)
