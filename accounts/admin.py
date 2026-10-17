from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "email_verified", "approved", "created_at")
    list_filter = ("email_verified", "approved")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    list_editable = ("approved",)
