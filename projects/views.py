import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from accounts.models import UserProfile
from .forms import ProjectForm
from .models import Project, ProjectMembership
from .permissions import profile_is_ready, visible_projects, can_manage_project, require_ready

@login_required
def dashboard(request):
    if not profile_is_ready(request.user):
        return render(request, "accounts/pending_approval.html")
    projects = visible_projects(request.user)
    return render(request, "projects/dashboard.html", {
        "total_projects": projects.count(),
        "mapped_projects": projects.filter(latitude__isnull=False, longitude__isnull=False).count(),
        "unmapped_projects": projects.filter(Q(latitude__isnull=True) | Q(longitude__isnull=True)).count(),
        "recent_projects": projects[:5],
    })

@login_required
def project_list(request):
    require_ready(request.user)
    projects = visible_projects(request.user)
    q = request.GET.get("q", "").strip()
    department = request.GET.get("department", "").strip()
    status = request.GET.get("status", "").strip()
    if q:
        projects = projects.filter(Q(title__icontains=q) | Q(code__icontains=q) | Q(description__icontains=q))
    if department:
        projects = projects.filter(department=department)
    if status:
        projects = projects.filter(status=status)
    departments = visible_projects(request.user).exclude(department="").values_list("department", flat=True).distinct()
    return render(request, "projects/project_list.html", {"projects": projects, "q": q, "department": department, "status": status, "departments": departments})

@login_required
def project_detail(request, pk):
    require_ready(request.user)
    project = get_object_or_404(visible_projects(request.user), pk=pk)
    return render(request, "projects/project_detail.html", {"project": project, "can_manage": can_manage_project(request.user, project), "files": project.attachments.all()})

@login_required
def project_create(request):
    require_ready(request.user)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            ProjectMembership.objects.get_or_create(project=project, user=request.user, defaults={"role": "manager"})
            messages.success(request, "Project created.")
            return redirect("project-detail", pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, "projects/project_form.html", {"form": form, "heading": "Create project"})

@login_required
def project_edit(request, pk):
    require_ready(request.user)
    project = get_object_or_404(visible_projects(request.user), pk=pk)
    if not can_manage_project(request.user, project):
        raise PermissionDenied
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated.")
            return redirect("project-detail", pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, "projects/project_form.html", {"form": form, "heading": "Edit project"})

@login_required
def project_map(request):
    require_ready(request.user)
    return render(request, "projects/map.html")

@login_required
def project_map_data(request):
    require_ready(request.user)
    projects = visible_projects(request.user).filter(latitude__isnull=False, longitude__isnull=False)
    results = [{
        "id": p.id, "title": p.title, "code": p.code, "department": p.department,
        "project_type": p.project_type, "status": p.status,
        "latitude": float(p.latitude), "longitude": float(p.longitude),
        "url": f"/projects/{p.pk}/",
    } for p in projects]
    return JsonResponse({"projects": results})

@login_required
def project_map_stats(request):
    require_ready(request.user)
    projects = visible_projects(request.user)
    total = projects.count()
    mapped = projects.filter(latitude__isnull=False, longitude__isnull=False).count()
    return JsonResponse({"total": total, "mapped": mapped, "unmapped": total - mapped})
