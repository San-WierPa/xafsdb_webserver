"""
urls.py
-----------------------
@author: Sebastian Paripsa
@email: paripsa@uni-wuppertal.de (or: sebastian.paripsa@gmail.com)
@linkedin: https://www.linkedin.com/in/sebastian-paripsa/
@git: https://github.com/San-WierPa
@orcid: https://orcid.org/0009-0000-3487-5399

SEO Tags:
---------
#SciCat #DatasetAutomation #Python #DataScience

Requirements:
-------------
- Python 3.10
- SciCat API access

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
