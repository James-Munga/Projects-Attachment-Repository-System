from django.conf import settings
from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("completed", "Completed"), ("on_hold", "On hold")]
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=120, blank=True)
    project_type = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="owned_projects")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ProjectMembership", related_name="project_memberships", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.code} — {self.title}"

    @property
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None

class ProjectMembership(models.Model):
    ROLE_CHOICES = [("manager", "Project manager"), ("contributor", "Contributor"), ("viewer", "Viewer")]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user} — {self.project} ({self.role})"
