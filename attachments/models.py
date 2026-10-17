import os
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from projects.models import Project

def attachment_upload_path(instance, filename):
    safe_name = os.path.basename(filename)
    return f"projects/{instance.project_id}/attachments/{safe_name}"

ALLOWED_EXTENSIONS = ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "csv", "txt", "zip", "tif", "tiff", "shp", "shx", "dbf", "prj", "geojson", "gpkg", "png", "jpg", "jpeg"]

class Attachment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="attachments")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to=attachment_upload_path, validators=[FileExtensionValidator(ALLOWED_EXTENSIONS)])
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title
