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
import logging
from typing import Type, List, Dict, Any, NoReturn

import scicat_py
from auto_dataset_create import AutoDatasetCreation
from auto_bl_create import AutoBlCreation
from django import forms
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseForbidden, HttpResponseNotFound,
                         HttpResponseServerError, HttpRequest)
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet

from webserver.settings import CONTEXT, EMAIL_HOST_USER
import json
import base64
import zipfile
import h5py
from io import BytesIO
import yaml

from ._auth_constants import CONFIGURATION
from .models import Files
from .serializers import FileCreateUpdateSerializer, FileSerializer
from .utils import get_access, get_all_datasets, term_checker, snake_case_to_title_case

from plugins.read_data import ReadData

def beamline_details(request, beamline_id: str) -> HttpResponse:
    """
    Retrieves information about the given beamline from the database and renders the beamline details page.

    Args:
        request: The HTTP request object.
        beamline_id: The ID of the beamline to retrieve information for.

    Returns:
        The rendered HTML page with information about the beamline.

    Raises:
        Redirects to an 'error' page if there is an error while retrieving the beamline information.
    """
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        # Assuming you have an API endpoint to fetch beamline metadata
        api_instance_beamline = scicat_py.InstrumentsApi(api_client)
        #try:
        beamline_metadata = api_instance_beamline.instruments_controller_find_one(id=beamline_id)
        #except Exception as e:
            # Handle exceptions and redirect to an error page or return an appropriate response
            #return redirect('error')

    # Render the beamline details using a Django template
    return render(request, 'landing/base_beamline.html', {'beamline_metadata': beamline_metadata})

def beamline_upload(request: HttpRequest) -> HttpResponse:
    """
    Renders the page for uploading a new beamline to the system.

    This view is responsible for presenting the form where users can input details
    to add a new beamline. It does not process form data itself; it only serves the
    initial HTML page containing the form.

    Parameters:
        request (HttpRequest): The HTTP request object that triggered this view.

    Returns:
        HttpResponse: An HttpResponse object that renders the 'addbeamline.html' template.

    No exceptions raised by this function directly; however, it relies on Django's internal
    mechanisms to locate and render the specified template.
    """
    return render(request, "landing/addbeamline.html")

@api_view(["POST"])
def add_beamline(request: HttpRequest) -> HttpResponse:
    """
    Processes a POST request to add a new beamline, ensuring the beamline name
    does not already exist in the database before creation.

    This function checks if a beamline with the specified name already exists in the
    system. If it exists, it redirects the user to an error page with a relevant
    message. If it does not exist, it proceeds to create the beamline using the provided
    metadata.

    Parameters:
        request (HttpRequest): The HTTP request object that contains the beamline name
        in its POST data.

    Returns:
        HttpResponse: Redirects to a 'thank_you' page upon successful creation or to
        an 'error' page if the beamline name already exists.

    Raises:
        Redirects occur based on the presence of the beamline name in the database.
        Specific exceptions from the API client or creation process are handled internally
        and result in redirection to error handling pages.

    Side effects:
        - Possible creation of a new beamline entry in the database if the name is unique.
        - Interaction with the SciCat API to fetch existing beamlines and compare names.
        - User feedback provided through messages indicating success or failure.
    """
    posted_beamline_name = request.POST.get('beamline', '')

    # Initialize API client and fetch existing beamlines
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token
        api_instance_dataset = scicat_py.InstrumentsApi(api_client)
        beamline_list = api_instance_dataset.instruments_controller_find_all()

        # Check if the posted beamline name already exists in the existing beamlines
        for instrument in beamline_list:
            # Safely check if custom_metadata exists and has the 'FACILITY' key
            if instrument.custom_metadata and 'FACILITY' in instrument.custom_metadata:
                facility_info = instrument.custom_metadata['FACILITY']
                # Use .get() to safely access 'beamline', providing a default of an empty string if not found
                existing_beamline_name = facility_info.get('beamline', '')

                # Proceed with comparison if existing_beamline_name is not an empty string
                if existing_beamline_name and posted_beamline_name.lower() == existing_beamline_name.lower():
                    # Beamline with the same name already exists, handle accordingly
                    messages.error(request, 'Beamline name already exists.')
                    return redirect("landing/error.html")
            else:
                # Optionally handle the case where instrument does not have the expected metadata structure
                print(f"Instrument {getattr(instrument, 'pid', 'Unknown ID')} does not have the expected custom_metadata structure.")



    # If the beamline name does not exist, proceed with creation
    AutoBlCreation(
        verify_beamline_meta=request.POST,
    )
    return redirect('thank_you')

def beamline_list(request: HttpRequest) -> HttpResponse:
    """
    Retrieves a list of all beamlines from the SciCat Instruments API and renders a
    web page to display these beamlines.

    This view connects to the SciCat Instruments API to fetch a complete list of beamline
    instruments. It then passes this list to the 'beamline_list.html' template for display.
    The view uses an API client configured with necessary authentication details to ensure
    secure access to the SciCat service.

    Parameters:
        request (HttpRequest): The HTTP request object that triggered this view, used
                               primarily by Django for handling the HTTP lifecycle.

    Returns:
        HttpResponse: An HttpResponse object that renders the 'beamline_list.html' template
                      with the beamline metadata passed as context.

    Side effects:
        - Makes a network request to the SciCat Instruments API to retrieve beamline data.
        - Relies on global configuration settings for API connectivity details.

    Note:
        This function assumes that the API client and authentication details are correctly
        set up and that the 'beamline_list.html' template exists and is correctly formatted
        to display the beamline data.
    """
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.InstrumentsApi(api_client)
        beamline_meta_list = api_instance_dataset.instruments_controller_find_all()
        #print(beamline_meta_list)
    return render(
        request,
        "landing/beamline_list.html",
        {"beamline_meta_list": beamline_meta_list},
    )


# render the file upload view and navigate to the html page
#@user_passes_test(lambda u: u.is_superuser)
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
        #print("I'm the temporary_uploaded_file:", temporary_uploaded_file)

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
            #print("File from dataset_upload:", file)
            file.write(decoded_file)
            file.close()

        if len(decoded_list) > 0:
            data = [
                str(data).split("\t") for data in decoded_list
            ]

            update_erange = request.POST
            #print("dataset_upload:", update_erange)
            reader = ReadData(update_erange=update_erange)
            dictionary = reader.extract_header(data_path="temp/" + dataset_name)
            #print("I'm here:", dictionary)
            context = {
                "decode_file_name": dataset_name,
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
    #print("FILE_path from verify_upload:", str(file_path))
    AutoDatasetCreation(
        s3_data_path="temp/" + str(file_path),
        data_set_name=file_path,
        verify_data=update_erange,
    )
    #dataset_id = adc.create_testdata()
    #return redirect("dataset_details", dataset_id=dataset_id)
    #return render(request, "landing/home.html")
    return redirect('thank_you')

    #except Exception as e:
    #    logger.exception("Error occurred while verifying upload: %s", str(e))
    #    return HttpResponseServerError("Error occurred while verifying upload")

@api_view(["POST"])
def approval_by_curator(request: HttpRequest, dataset_id: str) -> NoReturn:
    """
    Processes a POST request to update the approval status of a dataset based on curator's decision.

    This function updates the dataset's publication status and curator information in the SciCat
    database using the SciCat API. It captures the approval status and curator's username from the POST
    request, updates the dataset accordingly, and redirects to the curator's dataset list page.

    Parameters:
        request (HttpRequest): The HTTP request object containing POST data with the approval
                               status ('APPROVAL' or 'DISAPPROVAL') and the curator's username.
        dataset_id (str): The unique identifier of the dataset to update.

    Returns:
        Redirects to the 'dataset_list_curator' URL after successful update.

    Side effects:
        - Updates the 'is_published' status and 'updated_by' fields of the specified dataset
          in the SciCat database.
        - If an error occurs during the API interaction, it may redirect to an error handler
          or the operation may fail silently depending on global exception handling policies.

    Note:
        This function relies on proper configuration of the SciCat API client and correct API
        endpoint availability. It assumes that the dataset ID provided is valid and exists in the
        database.
    """
    if request.method == 'POST':
        approval_status = request.POST.get('approval_status') == 'APPROVAL'
        curator_info = request.POST.get('curator_updated_by')
        #print(f"Approval Status for dataset {dataset_id}: {approval_status}")

        with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
            access_token = get_access()
            api_client.configuration.access_token = access_token
            # Initialize API instance
            api_instance = scicat_py.DatasetsApi(api_client)

            update_dataset_dto = scicat_py.UpdateDatasetDto(
                is_published=approval_status,
                updated_by=curator_info
                )
            api_response = (
                    api_instance.datasets_controller_find_by_id_replace_or_create(
                        dataset_id,
                        update_dataset_dto,
                        async_req=False,
                        _preload_content=False,
                    )
                )
            #json.loads(api_response.data)
    return redirect('dataset_list_curator')

def thank_you(request: HttpRequest) -> HttpResponse:
    """
    Renders a "Thank You" page as a response to various user actions, typically following form submissions.

    This view simply returns the 'thank_you.html' template without any context or additional processing,
    serving as a straightforward acknowledgement or confirmation page after user submissions.

    Parameters:
        request (HttpRequest): The HTTP request object that triggered this view, used by Django
                               to handle the HTTP lifecycle.

    Returns:
        HttpResponse: An HttpResponse object that renders the 'thank_you.html' template.
    """
    return render(request, 'landing/thank_you.html')


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
        #print("Dataset Meta:" , dataset_meta)

        # Check if the user wants to download the metadata
        #if request.GET.get('download_metadata'):
        #    # Convert metadata to JSON formatted string
        #    metadata_json = json.dumps(dataset_meta, indent=4)
        #    # Create an HttpResponse object with the JSON data
        #    response = HttpResponse(metadata_json, content_type='application/json')
        #    # Set content disposition header for download prompt
        #    response['Content-Disposition'] = f'attachment; filename="{dataset_id}_metadata.json"'
        #    return response

        #if request.GET.get('download_metadata_hdf5'):
        ## Create an in-memory HDF5 file
        #    output = BytesIO()
        #    with h5py.File(output, 'w') as hf:
        #        for key, value in dataset_meta.items():
        #            hf.create_dataset(key, data=str(value))
        #    # Prepare HttpResponse
        #    output.seek(0)
        #    response = HttpResponse(output.read(), content_type='application/x-hdf5')
        #    response['Content-Disposition'] = f'attachment; filename="{dataset_id}_metadata.hdf5"'
#
        #    return response

        #if request.GET.get('download_metadata_yaml'):
        #    # Convert metadata to YAML formatted string
        #    metadata_yaml = yaml.dump(dataset_meta)
        #    # Create HttpResponse with YAML data
        #    response = HttpResponse(metadata_yaml, content_type='application/x-yaml')
        #    response['Content-Disposition'] = f'attachment; filename="{dataset_id}_metadata.yaml"'
#
        #    return response

        #if request.GET.get('download_text'):
        #    # Adding Sample Info section:
        #    content_str = "*Sample Info*:\n"
        #    content_str += f"    - ID: {dataset_meta.get('id', 'N/A')}\n"
        #    content_str += f"    - Dataset Name: {dataset_meta.get('datasetName', 'N/A')}\n"
        #    sample_info = dataset_meta['scientificMetadata']['sample_info']
        #    for key, value in sample_info.items():
        #        # Convert the key from snake_case to Title Case
        #        title_case_key = snake_case_to_title_case(key)
        #        content_str += f"    - {title_case_key}: {value}\n"
#
        #    # Adding Bibliography section
        #    content_str += "\n*Bibliography*:\n"
        #    bibliography = dataset_meta['scientificMetadata'].get('bibliography', {})
        #    content_str += f"    - Owner: {dataset_meta.get('owner', 'N/A')}\n"
        #    content_str += f"    - Institute: {dataset_meta.get('ownerGroup', 'N/A')}\n"
        #    content_str += f"    - Contact Email: {dataset_meta.get('contactEmail', 'N/A')}\n"
        #    for key, value in bibliography.items():
        #        # Convert the key from snake_case to Title Case
        #        title_case_key = snake_case_to_title_case(key)
        #        content_str += f"    - {title_case_key}: {value}\n"
#
        #    # Adding Instrument section
        #    content_str += "\n*Instrument*:\n"
        #    instrument = dataset_meta['scientificMetadata'].get('instrument', {})
        #    for key, value in instrument.items():
        #        # Convert the key from snake_case to Title Case
        #        title_case_key = snake_case_to_title_case(key)
        #        content_str += f"    - {title_case_key}: {value}\n"
#
        #    # Filter Files objects by dataset_id
        #    item_list = Files.objects.filter(dataset_id=dataset_id)
        #    for item in item_list:
        #        # Ensure there is a file associated with the item
        #        if item.file:
        #            # Reading the file content
        #            item.file.open('r')
        #            file_content = item.file.read()
        #            content_str += f"\nContent of {item.file_name}:\n{file_content}\n"
        #            item.file.close()
#
        #    # Creating the HttpResponse object with the content string
        #    response = HttpResponse(content_str, content_type='text/plain')
        #    response['Content-Disposition'] = f'attachment; filename="{dataset_id}_metaData.txt"'
        #    return response

        attachment_response = (
            api_instance_dataset.datasets_controller_find_all_attachments(dataset_id)
        )
        #print(len(attachment_response))
        #print(attachment_response)

        try:
            raw_data_fig = attachment_response[0].thumbnail
            normalized_data_fig = attachment_response[1].thumbnail
            k_fig = attachment_response[2].thumbnail
            R_fig = attachment_response[3].thumbnail
        # TODO:
        except IndexError:
            return redirect("error")

        if request.GET.get('download_zip'):
            zip_buffer = BytesIO()

            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Metadata as JSON
                metadata_json = json.dumps(dataset_meta, indent=4)
                zip_file.writestr(f"{dataset_id}_metadata.json", metadata_json)

                # Metadata as YAML
                metadata_yaml = yaml.dump(dataset_meta)
                zip_file.writestr(f"{dataset_id}_metadata.yaml", metadata_yaml)

                # Metadata as HDF5
                hdf5_buffer = BytesIO()
                with h5py.File(hdf5_buffer, 'w') as hf:
                    for key, value in dataset_meta.items():
                        hf.create_dataset(key, data=str(value))
                hdf5_buffer.seek(0)
                zip_file.writestr(f"{dataset_id}_metadata.hdf5", hdf5_buffer.read())

                # Detailed Metadata as Text
                # Adding Sample Info section:
                content_str = "*Sample Info*:\n"
                content_str += f"    - ID: {dataset_meta.get('id', 'N/A')}\n"
                content_str += f"    - Dataset Name: {dataset_meta.get('datasetName', 'N/A')}\n"
                sample_info = dataset_meta['scientificMetadata']['sample_info']
                for key, value in sample_info.items():
                    # Convert the key from snake_case to Title Case
                    title_case_key = snake_case_to_title_case(key)
                    content_str += f"    - {title_case_key}: {value}\n"

                # Adding Bibliography section:
                content_str += "\n*Bibliography*:\n"
                bibliography = dataset_meta['scientificMetadata'].get('bibliography', {})
                content_str += f"    - Owner: {dataset_meta.get('owner', 'N/A')}\n"
                content_str += f"    - Institute: {dataset_meta.get('ownerGroup', 'N/A')}\n"
                content_str += f"    - Contact Email: {dataset_meta.get('contactEmail', 'N/A')}\n"
                for key, value in bibliography.items():
                    # Convert the key from snake_case to Title Case
                    title_case_key = snake_case_to_title_case(key)
                    content_str += f"    - {title_case_key}: {value}\n"

                # Adding Instrument section:
                content_str += "\n*Instrument*:\n"
                instrument = dataset_meta['scientificMetadata'].get('instrument', {})
                for key, value in instrument.items():
                    # Convert the key from snake_case to Title Case
                    title_case_key = snake_case_to_title_case(key)
                    content_str += f"    - {title_case_key}: {value}\n"

                # Filter Files objects by dataset_id
                item_list = Files.objects.filter(dataset_id=dataset_id)
                for item in item_list:
                    # Ensure there is a file associated with the item
                    if item.file:
                        # Reading the file content
                        item.file.open('r')
                        file_content = item.file.read()
                        content_str += f"\nContent of {item.file_name}:\n{file_content}\n"
                        item.file.close()

                zip_file.writestr(f"{dataset_id}_metaData.txt", content_str)

                # List of your base64 encoded image strings with the prefix
                encoded_images = [raw_data_fig, normalized_data_fig, k_fig, R_fig]

                for index, encoded_img in enumerate(encoded_images):
                    if encoded_img:
                        # Strip the prefix and decode the base64 string to binary data
                        img_data = base64.b64decode(encoded_img.split("data:image/jpeg;base64,")[1])

                        # Write the decoded image data to the ZIP file as JPEG images
                        zip_file.writestr(f"plot{index+1}.jpg", img_data)

                # README content:
                content_text = (
                    "*Content description:*\n"
                    "\n"
                    "This zipfile contains 10 files (including this one):\n"
                    "\n"
                    "*1. README_FIRST*\n"
                    "\n"
                    "*2. README_ownership_and_usage_notice*\n"
                    "General information and usage\n"
                    "\n"
                    "*3. PID..._metaData.txt*\n"
                    "Contains all metadata from this dataset - HUMAN READABLE\n"
                    "+ content of the original datafile - including the values.\n"
                    "\n"
                    "*4. PID..._metadata.hdf5*\n"
                    "Contains all metadata. Format: hdf5 - MACHINE READABLE\n"
                    "\n"
                    "*5. PID..._metadata.json*\n"
                    "Contains all metadata. Format: json - MACHINE READABLE\n"
                    "\n"
                    "*6. PID..._metadata.yaml*\n"
                    "Contains all metadata. Format: yaml - MACHINE READABLE\n"
                    "\n"
                    "*7. plot1.jpg*\n"
                    "JPEG image of the Raw XAFS\n"
                    "\n"
                    "*8. plot2.jpg*\n"
                    "JPEG image of the Normalized XAFS\n"
                    "\n"
                    "*9. plot3.jpg*\n"
                    "JPEG image of Chi(k)\n"
                    "\n"
                    "*9. plot4.jpg*\n"
                    "JPEG image of Chi(R)\n"
                    "\n"
                    "NOTE: The size of all image windows can be changed!"
                )
                zip_file.writestr("README_FIRST.txt", content_text)

                # Ownership and usage notice text
                notice_text = (
                    "Thank you for using RefXAS.\n"
                    "Please be aware, do not misuse the data, cite properly when you use this data\n"
                    "and please always cite RefXAS!\n"
                    "For any questions, please write to paripsa@uni-wuppertal.de\n"
                    "\n"
                    "Thank you for supporting the RefXAS community."
                )
                # Write the notice text as a .txt file to the ZIP
                zip_file.writestr("README_ownership_and_usage_notice.txt", notice_text)

            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{dataset_id}_plots_and_meta_data.zip"'
            return response

        item_list: List[Dict[str, str]] = Files.objects.filter(dataset_id=dataset_id)

        # Check if beamline exits
        api_instance_dataset = scicat_py.InstrumentsApi(api_client)
        beamline_list = api_instance_dataset.instruments_controller_find_all()

        # Initialize an empty list to hold all beamline names
        all_beamline_data = []

        # Iterate over all instruments to extract their beamline names
        for instrument in beamline_list:
            # Safely check if custom_metadata exists and has the 'FACILITY' key
            if instrument.custom_metadata and 'FACILITY' in instrument.custom_metadata:
                facility_info = instrument.custom_metadata['FACILITY']
                beamline_name = facility_info.get('beamline')  # Use .get() for safe access
                beamline_id = getattr(instrument, 'pid', None)  # Use getattr for safe attribute access

                # Check if both beamline_name and beamline_id are not None
                if beamline_name and beamline_id:
                    all_beamline_data.append({'name': beamline_name, 'id': beamline_id})
            else:
                # Optionally handle the case where instrument does not have the expected metadata structure
                print(f"Instrument {getattr(instrument, 'pid', 'Unknown ID')} does not have the expected custom_metadata structure.")

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
            #"beamline_name": beamline_name,
            "all_beamline_data": all_beamline_data,
        },
    )

def dataset_list_curator(request: HttpRequest) -> HttpResponse:
    """
    Retrieves a list of datasets from the SciCat API and displays them on a
    curator-specific page with pagination.

    This view fetches datasets from the SciCat database using the SciCat API, applying
    no specific filters. It handles pagination of the datasets to ensure the page is
    not overloaded with data and improves user interface responsiveness.

    Parameters:
        request (HttpRequest): The HTTP request object that contains metadata such as
                               GET parameters used for pagination.

    Returns:
        HttpResponse: Renders the 'dataset_list_curator.html' with the paginated list of
                      datasets.

    Raises:
        PageNotAnInteger: If the page number in the GET request is not an integer, it defaults to the first page.
        EmptyPage: If the page number in the GET request is out of range (too high), it defaults to the last available page.

    Note:
        This function assumes that the API client setup and the necessary authentication are correctly configured.
        The presence of appropriate error handling for API interactions suggests any issues with API connectivity
        or data retrieval will default to handling within the Django template or a failover page scenario.
    """
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        filter = None
        dataset_meta_list = api_instance_dataset.datasets_controller_find_all(
            filter=filter
        )

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
        "landing/dataset_list_curator.html",
        {"dataset_meta_list": dataset_meta_list},
    )


def dataset_details_curator(request: HttpRequest, dataset_id: str) -> HttpResponse:
    """
    Retrieves detailed metadata and associated thumbnails for a specific dataset from the SciCat API,
    intended for curator review, and renders this information on a dedicated page.

    This view fetches comprehensive metadata for a given dataset by its ID, along with thumbnails
    of related data visualizations such as raw data figures and normalized data figures. It ensures
    that all necessary data for a complete curatorial review is available and handles the case where
    expected data might be missing by redirecting to an error page.

    Parameters:
        request (HttpRequest): The HTTP request object that triggered this view.
        dataset_id (str): The unique identifier of the dataset to retrieve.

    Returns:
        HttpResponse: Renders the 'base_curator.html' with detailed dataset metadata and
                      thumbnail images. If required thumbnails are missing, redirects to
                      an error page.

    Raises:
        IndexError: An exception is raised if the expected thumbnails are not found in the
                    attachment response, which triggers a redirect to an error handling page.

    Note:
        The function assumes that the dataset ID provided is valid and that the dataset exists
        in the database. Proper error handling must be in place to manage cases where the dataset
        ID might be incorrect or the dataset does not exist.
    """
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        dataset_meta = api_instance_dataset.datasets_controller_find_by_id(dataset_id)

        attachment_response = (
            api_instance_dataset.datasets_controller_find_all_attachments(dataset_id)
        )

        try:
            raw_data_fig = attachment_response[0].thumbnail
            normalized_data_fig = attachment_response[1].thumbnail
            k_fig = attachment_response[2].thumbnail
            R_fig = attachment_response[3].thumbnail
        # TODO:
        except IndexError:
            return redirect("error")

    return render(
        request,
        "landing/base_curator.html",
        {
            "dataset_meta": dataset_meta,
            "raw_data_fig": raw_data_fig,
            "normalized_data_fig": normalized_data_fig,
            "k_fig": k_fig,
            "R_fig": R_fig,
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


def team_contact(request) -> HttpResponse:
    """
    Render the team_contact page that combines both team description and contact form functionalities.

    - Team Description: Displays information about team members, their roles, and descriptions.
    - Contact Form: Allows users to send a message through a form.

    If the request method is "POST", validate the contact form data submitted by the user.
    If the form is valid, send an email to the site admin with the form data.
    If the email is successfully sent, redirect the user to the homepage.
    If the email fails to send, return an HTTP response indicating the error.

    If the request method is not "POST", render the page with a new ContactForm instance
    and the team description.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object, containing the rendered page,
        either with the contact form, team description, or a redirect to the homepage.

    Raises:
        BadHeaderError: If an invalid email header is found.
    """

    # Team description data
    team_description = [
        {'name': 'Sebastian Paripsa', 'role': 'Developer', 'contact': 'paripsa@uni-wuppertal.de'},
        {'name': 'Abhijeet Gaur', 'role': 'Senior Scientist', 'contact': ' abhijeet.gaur@kit.edu'},
        {'name': 'Frank Foerste', 'role': 'Developer', 'contact': 'ffoerste@physik.tu-berlin.de'},
        {'name': 'Christopher Schlesiger', 'role': 'Scientist', 'contact': ' christopher.schlesiger@tu-berlin.de'},
    ]

    # Handle contact form submission
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
            return redirect("thank_you")

    form = ContactForm()

    context = {
        "team_description": team_description,
        "form": form,
    }

    return render(request, "landing/team_contact.html", context)

