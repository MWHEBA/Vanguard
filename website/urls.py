from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("solutions/", views.solutions, name="solutions"),
    path("solutions/vancom/", views.solution_detail, {"slug": "vancom"}, name="vancom"),
    path("solutions/vulture-uavs/", views.solution_detail, {"slug": "vulture-uavs"}, name="vulture_uavs"),
    path("solutions/skyguard/", views.solution_detail, {"slug": "skyguard"}, name="skyguard"),
    path("solutions/tactical-data-link/", views.solution_detail, {"slug": "tactical-data-link"}, name="tactical_data_link"),
    path("contact/", views.contact, name="contact"),
]
