from django.urls import path
from . import views

urlpatterns = [
    path("project/<int:project_id>/upload/", views.attachment_upload, name="attachment-upload"),
    path("<int:pk>/download/", views.attachment_download, name="attachment-download"),
]
