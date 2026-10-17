from django.core.exceptions import PermissionDenied
from .models import Project, ProjectMembership

def profile_is_ready(user):
    if not user.is_authenticated or not user.is_active:
        return False
    if user.is_superuser or user.is_staff:
        return True
    try:
        profile = user.userprofile
    except Exception:
        return False
    return bool(profile.email_verified and profile.approved)

def visible_projects(user):
    qs = Project.objects.select_related("owner")
    if user.is_superuser or user.is_staff:
        return qs
    return qs.filter(projectmembership__user=user).distinct()

def can_manage_project(user, project):
    if user.is_superuser or user.is_staff or project.owner_id == user.id:
        return True
    return ProjectMembership.objects.filter(project=project, user=user, role="manager").exists()

def require_ready(user):
    if not profile_is_ready(user):
        raise PermissionDenied("Please verify your email and wait for administrator approval.")
