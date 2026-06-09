from django.contrib import admin

from .models import PickupNotification


@admin.register(PickupNotification)
class PickupNotificationAdmin(admin.ModelAdmin):
    list_display = ("parcel", "channel", "recipient", "status", "created_at")
    list_filter = ("channel", "status")
    search_fields = ("recipient", "parcel__tracking_no")
