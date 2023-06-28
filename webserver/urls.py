"""
@author: Sebastian Paripsa
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("xafsdb_web.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

handler400 = "xafsdb_web.views.bad_request"
handler403 = "xafsdb_web.views.permission_denied"
handler404 = "xafsdb_web.views.page_not_found"
handler500 = "xafsdb_web.views.server_error"
