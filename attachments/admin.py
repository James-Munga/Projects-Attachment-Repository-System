from django.contrib import admin
from .models import Attachment

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "uploaded_by", "uploaded_at")
    search_fields = ("title", "project__title", "project__code")
    list_filter = ("uploaded_at",)
