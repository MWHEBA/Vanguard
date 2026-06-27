from django.urls import path

from . import dashboard_views

app_name = "dashboard"

urlpatterns = [
    path("", dashboard_views.index, name="index"),
    path("login/", dashboard_views.DashboardLoginView.as_view(), name="login"),
    path("home/", dashboard_views.home_content, name="home_content"),
    path("inquiries/", dashboard_views.inquiries, name="inquiries"),
    path("inquiries/<int:pk>/", dashboard_views.inquiry_detail, name="inquiry_detail"),
    path("reports/", dashboard_views.reports, name="reports"),
    path("settings/", dashboard_views.settings, name="settings"),
    path("branding/", dashboard_views.branding, name="branding"),
    path("solutions/", dashboard_views.solutions, name="solutions"),
    path("solutions/<int:pk>/edit/", dashboard_views.solution_edit, name="solution_edit"),
    path("solutions/<int:pk>/gallery/upload/", dashboard_views.solution_gallery_upload, name="solution_gallery_upload"),
    path("solutions/<int:pk>/gallery/reorder/", dashboard_views.solution_gallery_reorder, name="solution_gallery_reorder"),
    path("solutions/<int:pk>/gallery/<int:visual_pk>/replace/", dashboard_views.solution_gallery_replace, name="solution_gallery_replace"),
    path("solutions/<int:pk>/gallery/<int:visual_pk>/title/", dashboard_views.solution_gallery_title, name="solution_gallery_title"),
    path("solutions/<int:pk>/gallery/<int:visual_pk>/delete/", dashboard_views.solution_gallery_delete, name="solution_gallery_delete"),
    path("users/", dashboard_views.users, name="users"),
    path("users/add/", dashboard_views.user_add, name="user_add"),
    path("users/<int:pk>/edit/", dashboard_views.user_edit, name="user_edit"),
]

