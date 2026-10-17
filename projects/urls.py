from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_list, name="project-list"),
    path("new/", views.project_create, name="project-create"),
    path("map/", views.project_map, name="project-map"),
    path("map/data/", views.project_map_data, name="project-map-data"),
    path("map/stats/", views.project_map_stats, name="project-map-stats"),
    path("<int:pk>/", views.project_detail, name="project-detail"),
    path("<int:pk>/edit/", views.project_edit, name="project-edit"),
]
