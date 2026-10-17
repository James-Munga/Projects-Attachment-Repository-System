from django.contrib import admin
from django.urls import path, include
from projects.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("accounts/", include("accounts.urls")),
    path("projects/", include("projects.urls")),
    path("attachments/", include("attachments.urls")),
]
