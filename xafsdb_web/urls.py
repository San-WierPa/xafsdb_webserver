"""
@author: Sebastian Paripsa
"""

from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from . import views
from .views import FileViewSets, SearchView

router = routers.DefaultRouter()
router.register(r"file", FileViewSets)

schema_view = get_schema_view(
    openapi.Info(
        title="Photographery API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("", views.home, name="home"),
    path("dataset/list", views.dataset_list, name="dataset_list"),
    path(
        "dataset/details/<str:dataset_id>",
        views.dataset_details,
        name="dataset_details",
    ),
    path("contact", views.contact, name="contact"),
    path("search/", SearchView.as_view(), name="pg_search"),
    path("file/", include(router.urls)),
    re_path(
        r"^api/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # quality control file upload feature related endpoints
    path("dataset/upload_view", views.dataset_upload_view, name="dataset_upload_view"),
    path("dataset/upload", views.dataset_upload, name="dataset_upload"),
    path("dataset/verify_upload", views.verify_upload, name="verify_upload"),
]
