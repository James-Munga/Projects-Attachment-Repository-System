from django.contrib import admin
from .models import Project, ProjectMembership

class MembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "department", "status", "owner", "latitude", "longitude")
    list_filter = ("status", "department", "project_type")
    search_fields = ("code", "title", "description")
    inlines = [MembershipInline]

@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "role")
    list_filter = ("role",)
    search_fields = ("project__title", "user__username", "user__email")
