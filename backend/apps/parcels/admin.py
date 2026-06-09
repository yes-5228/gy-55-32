from django.contrib import admin

from .models import Parcel


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ("tracking_no", "receiver_name", "receiver_phone", "locker_cell", "status", "stored_at")
    list_filter = ("status", "carrier")
    search_fields = ("tracking_no", "receiver_name", "receiver_phone", "pickup_code")
