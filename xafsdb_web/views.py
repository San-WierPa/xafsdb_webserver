"""
@author: Sebastian Paripsa
"""

from django import forms
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound,
                         HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

import scicat_py
from webserver.settings import CONTEXT, EMAIL_HOST_USER, URL_REST_API

from ._auth_constants import CONFIGURATION
from .models import Files
from .serializers import FileCreateUpdateSerializer, FileSerializer
from .utils import get_access, get_all_datasets, term_checker


async def dataset_list(request):
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        filter = None
        dataset_meta_list = api_instance_dataset.datasets_controller_find_all(
            filter=filter
        )
        # all_ids = [i['id'] for i in dataset_meta_list]
        ##print(all_ids)
        # all_attachment_responses = []
        # for dataset_id in all_ids:
        #    all_attachment_responses_list = api_instance_dataset.datasets_controller_find_all_attachments(dataset_id)
        #    all_attachment_responses.append(all_attachment_responses_list)
        #
        ##plot_div_list = []
        # for i in range(len(all_attachment_responses)):
        #    #print(all_attachment_responses[i][0].id)
        #    plot_div = (all_attachment_responses[i][0].thumbnail) #display_thumbnail
        # print(plot_div_list)
        # plot_div_list.append(plot_div)
        # print(plot_div)

        # for i in range(len(all_attachment_responses)):
        #    try:
        #        #print(all_attachment_responses[i][0].thumbnail)
        #        plot_div = display_thumbnail(all_attachment_responses[i])
        #    except IndexError:
        #        plot_div = 'null'

    return render(
        request,
        "landing/dataset_list.html",
        {
            "dataset_meta_list": dataset_meta_list,
            # "plot_div": plot_div,
        },
    )


def dataset_details(request, dataset_id: str):
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        dataset_meta = api_instance_dataset.datasets_controller_find_by_id(dataset_id)

        attachment_response = (
            api_instance_dataset.datasets_controller_find_all_attachments(dataset_id)
        )

        try:
            data_fig = attachment_response[0].thumbnail  # display_thumbnail
            # print(attachment_response[0].thumbnail)
            k_fig = attachment_response[1].thumbnail
            R_fig = attachment_response[2].thumbnail
        except IndexError:
            # return HttpResponse("Oops. Looks like you have note uploaded a picture yet.")
            return redirect("error")

        item_list = Files.objects.filter(dataset_id=dataset_id)
    return render(
        request,
        "landing/base.html",
        {
            "dataset_meta": dataset_meta,
            "data_fig": data_fig,
            "k_fig": k_fig,
            "R_fig": R_fig,
            "item_list": item_list,
        },
    )


class SearchView(TemplateView):
    template_name = "landing/search_datasets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        term = self.request.GET.get("term")
        paginated_by = 10

        allDatasets = get_all_datasets()
        datasetList = []
        for title in allDatasets:
            term_checker(title, term, datasetList)

        paginator = Paginator(datasetList, paginated_by)
        page = self.request.GET.get("page")
        datasetList = paginator.get_page(page)

        context["datasetList"] = datasetList

        return context


class FileViewSets(ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FileUploadParser]
    lookup_field = "pk"

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action in {"create", "partial_update", "update"}:
            serializer = FileCreateUpdateSerializer
        return serializer


def home(request):
    return render(request, "landing/home.html", CONTEXT)


def page_not_found(request, exception):
    return HttpResponseNotFound(
        render(
            request,
            "landing/error.html",
            CONTEXT
            | {
                "ERROR_CODE": "Error 404",
                "ERROR_DESCR": "Page not found.",
            },
        )
    )


def server_error(request):
    return HttpResponseServerError(
        render(
            request,
            "landing/error.html",
            CONTEXT
            | {
                "ERROR_CODE": "Error 500",
                "ERROR_DESCR": "Server error.",
            },
        )
    )


def bad_request(request, exception):
    return HttpResponseBadRequest(
        render(
            request,
            "landing/error.html",
            CONTEXT
            | {
                "ERROR_CODE": "Error 400",
                "ERROR_DESCR": "Bad request.",
            },
        )
    )


def permission_denied(request, exception):
    return HttpResponseForbidden(
        render(
            request,
            "landing/error.html",
            CONTEXT
            | {
                "ERROR_CODE": "Error 403",
                "ERROR_DESCR": "Permission denied.",
            },
        )
    )


def error(request, exception):
    return render(request, "landing/error.html", CONTEXT)


class ContactForm(forms.Form):
    first_name = forms.CharField(required=False, max_length=50, label="First name")
    last_name = forms.CharField(required=True, max_length=50, label="Last name")
    email_address = forms.EmailField(
        required=True, max_length=150, label="Email address"
    )
    message = forms.CharField(
        widget=forms.Textarea, required=True, max_length=2000, label="Your message"
    )


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email_address"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("home")

    form = ContactForm()
    return render(request, "landing/contact.html", {"form": form})
