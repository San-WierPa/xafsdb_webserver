"""
@author: Sebastian Paripsa
"""
from datetime import datetime
import logging
from typing import Type, List, Dict, Any

import scicat_py
from auto_dataset_create import AutoDatasetCreation
from django import forms
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound,
                         HttpResponseServerError, HttpRequest)
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from webserver.settings import CONTEXT, EMAIL_HOST_USER

from ._auth_constants import CONFIGURATION
from .models import Files
from .serializers import FileCreateUpdateSerializer, FileSerializer
from .utils import get_access, get_all_datasets, term_checker

from plugins.read_data import read_data

# render the file upload view and navigate to the html page
@user_passes_test(lambda u: u.is_superuser)
def dataset_upload_view(request) -> HttpResponse:
    """
    Renders the "upload.html" template with the provided context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered "upload.html" template.
    """
    return render(request, "landing/upload.html", CONTEXT)


# read the uploaded file and send the data to verify view
@api_view(["POST"])
def dataset_upload(request):
        '''
        Handles dataset file uploads from the user and processes the file content for further use.

        Args:
        request (HttpRequest): An HttpRequest object that contains metadata about the dataset file.

        Returns:
        context (dict): A dictionary containing decoded file name, description, and dictionary data,
        which is used for further processing and storage in the reference database.

        Example:
        The function is typically used within a webserver created using Django framework. It processes
        uploaded dataset files by decoding and extracting relevant information, preparing it for storage
        and further analysis.
        '''
    #try:
        temporary_uploaded_file = request.FILES.get("file")
        print("I'm the temporary_uploaded_file:", temporary_uploaded_file)

        if temporary_uploaded_file is None:
            dataset_name = request.POST.get("dataset_name")
            if str(dataset_name).split("/")[-1].split(".")[-1] != "h5":
                readout_type = "r"
            else:
                readout_type = "rb"
            with open("temp/" + dataset_name, readout_type) as f:
                decoded_list = f.readlines()
            #if dataset_name is not None:
            #    temporary_uploaded_file.name = dataset_name
            #else:
            #    error_msg = json.dumps({"detail": "Please add a file before click upload"})
            #    return HttpResponse(error_msg, status=500)
            #return redirect("landing/error.html")
        else:
            if str(temporary_uploaded_file).split("/")[-1].split(".")[-1] != "h5":
                write_type = "w"
                decoded_file = temporary_uploaded_file.read().decode("utf-8")
            else:
                write_type = "wb"
                decoded_file = temporary_uploaded_file.read()
            dataset_name = temporary_uploaded_file.name
            decoded_list = str(decoded_file).split("\r\n")
            #print(decoded_list)

            # save file in temp folder
            file = open("temp/" + temporary_uploaded_file.name, write_type)
            print("File from dataset_upload:", file)
            file.write(decoded_file)
            file.close()

        if len(decoded_list) > 0:
            data = [
                str(data).split("\t") for data in decoded_list
            ]

            update_erange = request.POST
            print("dataset_upload:", update_erange)
            reader = read_data(update_erange=update_erange)
            dictionary = reader.extract_header(data_path="temp/" + dataset_name)
            #print("I'm here:", dictionary)
            context = {
                "decode_file_name": dataset_name,
                #"description": "{0} uploaded {1}".format(
                #    dataset_name, str(datetime.now())
                #),
                #"summary": "Uploaded File: "
                #+ str(dataset_name)
                #+ " has "
                #+ " array columns with "
                #+ str(len(data) - 1)
                #+ " data rows.",
                ### pass the dictionary to the template context
                "dictionary": dictionary,
                }
            #print("Context:", context)

            return render(request, "landing/verify.html", context)
    # TODO:
    #except Exception as e:
    #    error_msg = json.dumps({"detail": "Internal Server Error _" + str(e)})
    #    return HttpResponse(error_msg, status=500)


@api_view(["POST"])
def verify_upload(request) -> HttpResponse:
    """
    This function handles the verification process of an uploaded dataset on the webserver.
    It takes a POST request containing the dataset name and a flag for updating the energy range
    (update_erange). The function initiates an AutoDatasetCreation instance with the provided
    information and returns a HttpResponse upon successful verification.

    Args:
    request (HttpRequest): The POST request containing the dataset name and the update_erange flag.

    Returns:
    HttpResponse: Returns a HttpResponse rendering the home page if the verification is successful.
                  If an error occurs during the verification process, it returns a
                  HttpResponseServerError with an error message.

    """
    logger = logging.getLogger(__name__)
    #try:
    #verify_data = request.POST
    #print("verify_data:", verify_data)
    update_erange = request.POST
    #print("update_erange:", update_erange)
    file_path = request.POST.get("dataset_name")
    print("FILE_path from verify_upload:", str(file_path))
    AutoDatasetCreation(
        s3_data_path="temp/" + str(file_path),
        data_set_name=file_path,
        verify_data=update_erange,
    )
    #dataset_id = adc.create_testdata()
    #return redirect("dataset_details", dataset_id=dataset_id)
    return render(request, "landing/home.html")

    #except Exception as e:
    #    logger.exception("Error occurred while verifying upload: %s", str(e))
    #    return HttpResponseServerError("Error occurred while verifying upload")


def dataset_list(request) -> HttpResponse:
    """
    View function that retrieves a list of all datasets from the SciCat API
    and displays them in a paginated HTML view.

    Args:
        request: HttpRequest object representing the incoming request

    Returns:
        HttpResponse object representing the HTTP response that will be sent
        back to the client
    """
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        filter = None
        dataset_meta_list = api_instance_dataset.datasets_controller_find_all(
            filter=filter
        )

        ### Just for development reason:
        debug_data: Dict[str, str] = {"dataset_id": "1"}
        ###

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


def dataset_details(request, dataset_id: str) -> HttpResponse:
    """
    Retrieves information about the given dataset from scicat and renders the dataset details page with the
    relevant information.

    Args:
        request: The HTTP request object.
        dataset_id: The ID of the dataset to retrieve information for.

    Returns:
        The rendered HTML page with information about the dataset.

    Raises:
        Redirects to the 'error' page if there is an error while retrieving information about the dataset.
    """
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        dataset_meta = api_instance_dataset.datasets_controller_find_by_id(dataset_id)
        print("Dataset Meta:" , dataset_meta)

        attachment_response = (
            api_instance_dataset.datasets_controller_find_all_attachments(dataset_id)
        )
        print(len(attachment_response))
        print(attachment_response)

        try:
            raw_data_fig = attachment_response[0].thumbnail
            normalized_data_fig = attachment_response[1].thumbnail
            k_fig = attachment_response[2].thumbnail
            R_fig = attachment_response[3].thumbnail
        # TODO:
        except IndexError:
            return redirect("error")

        item_list: List[Dict[str, str]] = Files.objects.filter(dataset_id=dataset_id)
    return render(
        request,
        "landing/base.html",
        {
            "dataset_meta": dataset_meta,
            "raw_data_fig": raw_data_fig,
            "normalized_data_fig": normalized_data_fig,
            "k_fig": k_fig,
            "R_fig": R_fig,
            "item_list": item_list,
        },
    )


class SearchView(TemplateView):
    """
    A view for searching datasets by term.

    Attributes:
        template_name (str): The name of the template to render.
    """

    template_name = "landing/search_datasets.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Retrieves the context data for rendering the template.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            A dictionary of context data for rendering the template.
        """

        context: Dict[str, Any] = super().get_context_data(**kwargs)
        request: HttpRequest = self.request
        term: str = request.GET.get("term")
        paginated_by: int = 10

        allDatasets: List[Dict[str, Any]] = get_all_datasets()
        datasetList: List[Dict[str, Any]] = []
        for title in allDatasets:
            term_checker(title, term, datasetList)

        paginator: Paginator = Paginator(datasetList, paginated_by)
        page: str = self.request.GET.get("page")
        datasetList = paginator.get_page(page)

        context["datasetList"] = datasetList

        return context


class FileViewSets(ModelViewSet):
    """
    Viewset for managing files uploaded to the system.

    The viewset supports CRUD (Create, Retrieve, Update, Delete) operations
    for files, with support for uploading files via the MultiPartParser or
    FileUploadParser. The default serializer used is `FileSerializer`, which
    provides basic read-only functionality. For write operations, the
    `FileCreateUpdateSerializer` serializer is used, which provides additional
    validation and serialization/deserialization of uploaded files.

    The `lookup_field` attribute is set to `"pk"`, which is the primary key
    field used for looking up files.

    Methods
    -------
    get_serializer_class(self)
        Returns the serializer class to use for the current request, depending
        on the HTTP method used.
    """
    queryset: Type[Files] = Files.objects.all()
    serializer_class: Type[FileSerializer] = FileSerializer
    parser_classes = [MultiPartParser, FileUploadParser]
    lookup_field: str = "pk"

    def get_serializer_class(self) -> Type[FileSerializer]:
        serializer: Type[FileSerializer] = self.serializer_class
        if self.action in {"create", "partial_update", "update"}:
            serializer = FileCreateUpdateSerializer
        return serializer


def home(request: HttpRequest) -> HttpResponse:
    """
    Renders the home page of the website.

    Type request:
        HttpRequest

    Returns:
        The HTTP response object containing the rendered template.
    """
    return render(request, "landing/home.html", CONTEXT)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponseNotFound:
    """
    Handler for page not found (404) errors.

    Args:
        request (HttpRequest): The request that triggered the error.
        exception (Exception): The exception that was raised.

    Returns:
        HttpResponseNotFound: A rendered HTTP response with the error details.
    """
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


def error(request: HttpRequest, exception: Exception) -> HttpResponse:
    """
    View for rendering an error page when an exception is raised.

    Returns:
        The HTTP response containing the error page.
    """
    return render(request, "landing/error.html", CONTEXT)


class ContactForm(forms.Form):
    """
    A Django form for contacting the website owner.

    Fields:
    - first_name: Optional string field for the user's first name.
    - last_name: Required string field for the user's last name.
    - email_address: Required email field for the user's email address.
    - message: Required text field for the user's message.

    Usage example:

    form = ContactForm(request.POST)
    if form.is_valid():
        # Process the form data
        ...
    else:
        # Render the form with error messages
        ...
    """
    first_name = forms.CharField(required=False, max_length=50, label="First name",
                                 widget=forms.TextInput(attrs={'style': 'color: black;'}))
    last_name = forms.CharField(required=True, max_length=50, label="Last name",
                                widget=forms.TextInput(attrs={'style': 'color: black;'}))
    email_address = forms.EmailField(
        required=True, max_length=150, label="Email address",
        widget=forms.EmailInput(attrs={'style': 'color: black;'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'style': 'color: black;'}),
        required=True, max_length=2000, label="Your message"
    )


def contact(request):
    """
    Render the contact page and handle the contact form submission.

    If the request method is "POST", validate the form data submitted
    by the user. If the form is valid, send an email to the site admin
    with the form data. If the email is successfully sent, redirect the
    user to the homepage. If the email fails to send, return an HTTP
    response indicating the error.

    If the request method is not "POST", render the contact page with a
    new ContactForm instance.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object, containing the rendered
        contact page or a redirect to the homepage.

    Raises:
        BadHeaderError: If an invalid email header is found.
    """
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
