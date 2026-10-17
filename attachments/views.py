from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import UserProfile
from projects.models import Project
from projects.permissions import profile_is_ready, visible_projects, can_manage_project, require_ready
from .forms import AttachmentForm
from .models import Attachment

@login_required
def attachment_upload(request, project_id):
    require_ready(request.user)
    project = get_object_or_404(visible_projects(request.user), pk=project_id)
    if not can_manage_project(request.user, project):
        membership = project.projectmembership_set.filter(user=request.user, role="contributor").exists()
        if not membership:
            raise PermissionDenied
    if request.method == "POST":
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.project = project
            attachment.uploaded_by = request.user
            attachment.save()
            messages.success(request, "File uploaded.")
            return redirect("project-detail", pk=project.pk)
    else:
        form = AttachmentForm()
    return render(request, "attachments/upload.html", {"form": form, "project": project})

@login_required
def attachment_download(request, pk):
    require_ready(request.user)
    attachment = get_object_or_404(Attachment.objects.select_related("project"), pk=pk)
    if not visible_projects(request.user).filter(pk=attachment.project_id).exists():
        raise PermissionDenied
    try:
        attachment.file.open("rb")
    except (FileNotFoundError, OSError):
        raise Http404("File is unavailable.")
    return FileResponse(attachment.file, as_attachment=True, filename=attachment.file.name.split("/")[-1])
