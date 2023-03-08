"""
@author: Sebastian Paripsa
"""
import json
import sys
from datetime import datetime

import scicat_py
from auto_dataset_create import AutoDatasetCreation
from django import forms
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound,
                         HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from webserver.settings import CONTEXT, EMAIL_HOST_USER, URL_REST_API

from ._auth_constants import CONFIGURATION
from .models import Files
from .serializers import FileCreateUpdateSerializer, FileSerializer
from .utils import get_access, get_all_datasets, term_checker


# render the file upload view and navigate to the html page
def dataset_upload_view(request):
    return render(request, "landing/upload.html", CONTEXT)


# read the uploaded file and send the data to verify view
@api_view(["POST"])
def dataset_upload(request):
    try:
        temporary_uploaded_file = request.FILES.get("file")

        if temporary_uploaded_file is None:
            error_msg = json.dumps({"detail": "Please add a file before click upload"})
            return HttpResponse(error_msg, status=500)

        decoded_file = temporary_uploaded_file.read().decode("utf-8")
        decoded_list = str(decoded_file).split("\r\n")

        # save file in temp folder
        file = open("temp/" + temporary_uploaded_file.name, "w")
        file.write(decoded_file)
        file.close()

        if len(decoded_list) > 0:
            data = [
                str(data).split("\t") for data in decoded_list if data.startswith("#")
            ]
            headers = data[0]
            context = {
                "headers": headers,
                "decode_file_name": temporary_uploaded_file.name,
                "description": "{0} uploaded {1}".format(
                    temporary_uploaded_file.name, str(datetime.now())
                ),
                "summary": "Uploaded File: "
                + str(temporary_uploaded_file.name)
                + " has "
                + str(len(headers))
                + " array columns with "
                + str(len(data) - 1)
                + " data rows.",
            }

            return render(request, "landing/verify.html", context)

    except Exception as e:
        error_msg = json.dumps({"detail": "Internal Server Error _" + str(e)})
        return HttpResponse(error_msg, status=500)


@api_view(["POST"])
def verify_upload(request):
    try:
        verify_data = request.POST
        file_path = request.POST.get("dataset_name")
        AutoDatasetCreation(
            s3_data_path="temp/" + file_path,
            data_set_name=file_path,
            verify_data=verify_data,
        )
        return render(request, "landing/home.html")

    except Exception as e:
        error_msg = json.dumps({"detail": "Internal Server Error _" + str(e)})
        return HttpResponse(error_msg, status=500)


async def dataset_list(request):
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        filter = None
        dataset_meta_list = api_instance_dataset.datasets_controller_find_all(
            filter=filter
        )

        debug_data = {"dataset_id": "1"}

        page = request.GET.get("page", 1)
        paginator = Paginator(dataset_meta_list, 15)
        try:
            dataset_meta_list = paginator.page(page)
        except PageNotAnInteger:
            dataset_meta_list = paginator.page(1)
        except EmptyPage:
            dataset_meta_list = paginator.page(paginator.num_pages)

    return render(
        request,
        "landing/dataset_list.html",
        {"dataset_meta_list": dataset_meta_list, "debug_data": debug_data},
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
            data_fig = attachment_response[0].thumbnail
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
