from django.urls import path

from . import views
from .views import SearchView

urlpatterns = [
    path("", views.home, name="home"),
    path("dataset/list", views.dataset_list, name="dataset_list"),
    path("dataset/details/<str:dataset_id>", views.dataset_details, name="dataset_details"),
    path("contact", views.contact, name="contact"),
    path("search/", SearchView.as_view(), name="pg_search"),
]
