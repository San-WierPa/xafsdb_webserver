##############################################################################
### XRF ###
##############################################################################

"""
views.py
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

##############################################################################
### import packages ###
##############################################################################
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import render


#import scicat_py
#from webserver.settings import CONTEXT, EMAIL_HOST_USER


#def xrf_home(request: HttpRequest) -> HttpResponse:
#    """
#    Renders the home page of the website.
#
#    Type request:
#        HttpRequest
#
#    Returns:
#        The HTTP response object containing the rendered template.
#    """
#    return render(request, "landing_xrf/home.html",) #CONTEXT