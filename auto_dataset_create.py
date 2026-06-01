"""
auto_dataset_create.py
-----------------------
@author: Sebastian Paripsa
@email: paripsa@uni-wuppertal.de (or: sebastian.paripsa@gmail.com)
@linkedin: https://www.linkedin.com/in/sebastian-paripsa/
@git: https://github.com/San-WierPa

Description:
------------
This script automates the process of dataset creation by using the SciCat API.
It performs tasks such as data reading, quality control checks, and finally,
uploads the dataset to the designated repository.

SEO Tags:
---------
#SciCat #DatasetAutomation #Python #DataScience

Modules:
--------
- read_data: Reads the raw data files
- check_quality: Performs quality control on the dataset
- scicat_py: SciCat's Python API

Requirements:
-------------
- Python 3.10
- SciCat API access

"""

from __future__ import print_function

import json
import logging
import os
from datetime import datetime
from sys import path
from typing import Any, Dict, NoReturn, Optional

import environ
import numpy as np
import pyshorteners
import requests
from django.core.mail import send_mail

import scicat_py
from plugins.read_data import read_data
from quality_control.quality_check import check_quality
from webserver.settings import EMAIL_HOST_USER

env = environ.Env()
environ.Env.read_env()

prefix = env("PREFIX", default="file")


class AutoDatasetCreation(object):
    """
    This class automatically creates, respectively updates a dataset,
    does the quality_control and serves all to the webserver
    """

    def __init__(self, s3_data_path, data_set_name, verify_data):
        self.data_set_name = data_set_name
        # print("data_set_name:", data_set_name)
        self.s3_data_path = s3_data_path
        # print("s3_data_path:", s3_data_path)
        self.verify_data = verify_data

        # print("Dataset creation initialized...how exciting!")
        self.configuration = scicat_py.Configuration(
            # production
            host=os.getenv("SCICAT_BASE_URL", "http://scicat:3000"),
            # dev (varies due to shut-down/restart of vm - every restart changes ip)
            #host="http://34.29.27.51",
            # local server
            #host = "http://localhost:8000",
            # ubuntu
            #host = "http://172.27.20.173",
        )
        self.qc_path = "quality_control/"
        path.append(self.qc_path)
        self.auth_login()
        self.create_testdata()
        self.post_sthree()
        self.short_url()
        self.qc_and_update()
        self.upload_figure_data(
            figure=self.data_dict["scientific_metadata"]["Figures"]["raw_data"],
            caption="Raw data",
        )
        self.upload_figure_data(
            figure=self.data_dict["scientific_metadata"]["Figures"]["normalized_data"],
            caption="Normalized data",
        )
        self.upload_figure_data(
            figure=self.data_dict["scientific_metadata"]["Figures"]["k"], caption="k"
        )
        self.upload_figure_data(
            figure=self.data_dict["scientific_metadata"]["Figures"]["R"], caption="R"
        )

    def auth_login(self) -> Optional[str]:
        """
        Authenticates with the SciCat API by logging in with provided credentials
        and retrieves an access token for subsequent requests.

        Returns:
            The access token string or None (hence the Optional[str]) if there was an error
        """
        with scicat_py.ApiClient(configuration=self.configuration) as api_client:
            api_instance = scicat_py.AuthApi(api_client)
            credentials_dto = scicat_py.CredentialsDto(
                username=env("USERNAME_AUTH"),
                password=env("PASSWORD_AUTH"),
            )
            api_response = api_instance.auth_controller_login(credentials_dto)
            self.access_token = api_response["access_token"]
            print("ME ACCESS TOKEN:", self.access_token)
            return self.access_token

    def create_testdata(self) -> Optional[str]:
        """
        Creates a new test dataset and returns its ID.

        Returns:
            str or None: The ID of the created dataset or None if an error occurred.
        """
        titlename = self.data_set_name
        self.data_dict = {
            "owner_group": self.verify_data.get("Owner group"),
            "access_groups": "NO_THUMBNAIL",
            "creation_location": "wuppertal",
            "principal_investigator": "someone",
            "dataset_name": titlename
            + " "
            + datetime.now().strftime("%Y-%m-%d-%H_%M_%S"),
            "type": "raw",
            "is_published": False,
            "creation_time": str(datetime.now().isoformat()),
            "source_folder": "None",
            "owner": self.verify_data.get("Owner"),
            "contact_email": self.verify_data.get("Contact email"),
            "scientific_metadata": {
                "Description": self.verify_data.get("Description"),
                "Data": {
                    "Source": self.verify_data.get("Source"),
                    "Mode": self.verify_data.get("Measurement Mode"),
                    # TODO:
                    # "Energy": "None", # actual value
                    # "EnergyColumn": self.verify_data.get("Energy Column"), # description
                    # "Mu": "None", # actual value
                    # "MuColumn": self.verify_data.get("Mu Column"), # description
                    # "I_zero": "None", # actual value
                    # "I_zeroColumn": self.verify_data.get("I0 Column"), # description
                    # "Transmission": "None", # actual value
                    # "TransmissionColumn": self.verify_data.get("Transmission Column"), # description
                },
                "RAW": {
                    "edge_step": {
                        "value": 0.0,
                        "unit": "a.u.",
                        "documentation": "Height of the detected edge step.",
                    },
                    "k_max": {
                        "value": 0.0,
                        "unit": "\u212B\u207B\u00B9",
                        "documentation": "Considered angular wavenumber.",
                    },
                    "energy_resolution": {
                        "value": 0.0,
                        "unit": "eV",
                        "documentation": "Energy resolution of the measured spectrum in eV.",
                    },
                    "noise": {
                        "value": 0.0,
                        "unit": "a.u.",
                        "documentation": "Noise of the measurement.",
                    },
                    "edge_energy": {
                        "value": 0.0,
                        "unit": "eV",
                        "documentation": "Energy of the detected edge [eV].",
                    },
                },
                "PROCESSED": {
                    "amplitude_reduction_factor": {
                        "Z_ranges": {
                            "tentoforty": {
                                "value": 0.0,
                            },
                            "fortytoeighty": {
                                "value": 0.0,
                            },
                        },
                        "unit": "a.u.",
                        "documentation": "amplitude factor from the processed spectrum",
                    }
                },
                "Figures": {
                    "raw_data": None,
                    "normalized_data": None,
                    "k": None,
                    "R": None,
                },
                "sample_info": {
                    "coll_code": self.verify_data.get("Coll.code"),
                    "physical_state": self.verify_data.get("Phys.state"),
                    "crystal_orientation": self.verify_data.get("Crystal orientation"),
                    "temperature": self.verify_data.get("Temperature"),
                    "pressure": self.verify_data.get("Pressure"),
                    "sample_environment": self.verify_data.get("Sample environment"),
                    "general_remarks": self.verify_data.get("General remarks"),
                    "sample_prep": self.verify_data.get("Sample preparation"),
                    "sample_id": self.verify_data.get("Sample ID"),
                },
                "instrument": {
                    "facility": self.verify_data.get("Facility"),
                    "beamline": self.verify_data.get("Beamline"),
                    "aquisition_mode": self.verify_data.get("Acq. mode"),
                    "crystals": self.verify_data.get("Crystals"),
                    "mirrors": self.verify_data.get("Mirrors"),
                    "detectors": self.verify_data.get("Detectors"),
                    "element_input": self.verify_data.get("Element"),
                    "edge_input": self.verify_data.get("Edge"),
                    "max_k_range": self.verify_data.get("Max k-range"),
                },
                "bibliography": {
                    "doi": self.verify_data.get("DOI"),
                    "reference": self.verify_data.get("Reference"),
                    "disclaimer": self.verify_data.get("DisclaimerVerification"),
                },
                "is_approved": False,
            },
            "keywords": "None",
        }

        with scicat_py.ApiClient(self.configuration) as api_client:
            api_client.configuration.access_token = self.access_token
            api_instance = scicat_py.DatasetsApi(api_client)
            create_dataset_dto = scicat_py.CreateDatasetDto(**self.data_dict)
            api_response = api_instance.datasets_controller_create(
                create_dataset_dto, async_req=False, _preload_content=False
            )
            self.resp = json.loads(api_response.data)
            print("ME RAW DATA:", self.resp)
            self.datasetId = self.resp["id"]
            print("ME DATASET ID:", self.datasetId)
            return self.datasetId

    def post_sthree(self) -> requests.Response:
        """
        Uploads a file to the S3 bucket and returns the response.

        Returns:
            requests.Response: The response from the server.

        Raises:
            FileNotFoundError: If the file specified by `self.s3_data_path` is not found.
        """
        try:
            files = {"file": open(self.s3_data_path, "rb")}
            values: Dict[str, Any] = {"dataset_id": self.datasetId}
            # production:
            self.responds = requests.post(
                os.getenv("XAFSDB_FILE_API_URL", f"http://xafsdb:8000/{prefix}/{prefix}/"), files=files, data=values
            )
            # dev:
            #self.responds = requests.post(
            #   f"http://34.29.27.51/{prefix}/{prefix}/", files=files, data=values
            #)
            # local server
            #self.responds = requests.post(
            #    f"http://172.27.20.173/{prefix}/{prefix}/", files=files, data=values
            #)
            # print("I'm in sthree:", self.responds.json)
            return self.responds
        except FileNotFoundError as e:
            logging.exception(f"Could not upload file: {e}")
            raise

    def short_url(self) -> str:
        """
        Generate a short URL for the current file.

        Note: creates folder and downloads the file.
        Param:
            cache_ttl=0
            Disables caching and prevents the creation of any cache directory.
            May affect the performance of the application.

        Returns:
            The generated short URL as a string.
        """
        # self.short_url = self.responds.json()["file"].split("?")[0]
        type_tiny = pyshorteners.Shortener()
        # print("I'm in short_url:", self.responds.status_code, self.responds.text)
        self.short_url = type_tiny.tinyurl.short(self.responds.json()["file"])

        return self.short_url

    def qc_and_update(self) -> NoReturn:
        """
        Performs quality control checks on newly uploaded dataset measurements, updates
        the dataset's scientific metadata with quality control results, and communicates
        these updates to the SciCat database. Additionally, it generates and stores plots
        for the dataset and notifies the curator about the new dataset via email.

        Attributes:
            configuration: Configuration settings for the SciCat API client.
            access_token: Auth token used for API requests.
            qc_path: Path to the directory containing the quality control criteria JSON.
            verify_data: Dictionary containing data verification details used in quality checks.
            s3_data_path: Path where the dataset's files are stored, used for processing.
            data_dict: Dictionary where processed data and metadata are stored and updated.

        Uses:
            This method processes the dataset using predefined quality criteria stored in a
            JSON file, updates the dataset's metadata based on the analysis results, and uploads
            the updated information along with generated plots to the SciCat database. If all
            quality checks are passed, it sends an email to notify the curator and updates the
            dataset entry in the database with quality metrics and plot data.

        Raises:
            Various exceptions related to file handling, data processing, or API communication
            failures could be raised implicitly within the method.

        Side effects:
            - Modifies `self.data_dict` with new scientific metadata.
            - Generates plot images and encodes them in base64 for storage.
            - Sends an email to the curator.
            - Updates the dataset in the SciCat database with new information.
        """
        with scicat_py.ApiClient(self.configuration) as api_client:
            api_client.configuration.access_token = self.access_token
            api_instance = scicat_py.DatasetsApi(api_client)

            ### CHECK QUALITY CONTROL ###
            ### loading the json criteria file for reference
            cq_json = self.qc_path + "Criteria.json"
            ### initialize quality check object
            cq = check_quality(quality_criteria_json=cq_json)
            qc_list = []  ### this list will contain the quality criteria
            ### here the measurement data has to be forwarded, where will the data be stored in SciCat?
            # meas_data = np.loadtxt(self.short_url, skiprows=1)
            rd = read_data(update_erange=self.verify_data)
            rd.process_data(self.s3_data_path)
            # print("Meas_data from qc_and_update:", meas_data)
            cq.load_data(
                rd.data,
                source=self.data_dict["scientific_metadata"]["Data"]["Source"],
                name=self.data_dict["dataset_name"],
            )
            ### perform preprocessing on the data
            data = (
                cq.preprocess_data(take_first=True)
            )  #: data is a larch group with calibrated_energy = data.energy and absorption data.mu
            # TODO: print(data) and send to download (here mu and energy)
            ### plot the data and return the figure object
            # TODO: cache k and R - in der cq.data.R/k
            fig_raw_data = cq.plot_data(data_type="RAW")
            fig_normalized_data = cq.plot_data(data_type="NORMALIZED")
            fig_k = cq.plot_data(
                data_type="k"
            )  ### plot data in k and return the figure object
            fig_R = cq.plot_data(
                data_type="R"
            )  ### plot data in R and return the figure object
            self.data_dict["scientific_metadata"]["Figures"][
                "raw_data"
            ] = cq.encode_base64_figure(fig_raw_data)
            self.data_dict["scientific_metadata"]["Figures"][
                "normalized_data"
            ] = cq.encode_base64_figure(fig_normalized_data)
            self.data_dict["scientific_metadata"]["Figures"][
                "k"
            ] = cq.encode_base64_figure(fig_k)
            self.data_dict["scientific_metadata"]["Figures"][
                "R"
            ] = cq.encode_base64_figure(fig_R)
            ### check for the edge step
            qc_list.append(cq.check_edge_step())
            ### add to data_dict
            self.data_dict["scientific_metadata"]["RAW"]["edge_energy"][
                "value"
            ] = np.round(data.e0, decimals=1)
            ### add to data_dict
            self.data_dict["scientific_metadata"]["RAW"]["edge_step"][
                "value"
            ] = np.round(qc_list[0][1], decimals=3)
            ### check for the energy resolution
            qc_list.append(cq.check_energy_resolution())
            ### add to data_dict
            self.data_dict["scientific_metadata"]["RAW"]["energy_resolution"][
                "value"
            ] = np.round(qc_list[1][1], decimals=1)
            ### check for k
            qc_list.append(cq.check_k())
            ### add to data_dict
            self.data_dict["scientific_metadata"]["RAW"]["k_max"]["value"] = np.round(
                qc_list[2][1], decimals=1
            )
            ### Hand over quality criteria to webserver
            self.edge_step = self.data_dict["scientific_metadata"]["RAW"]["edge_step"][
                "value"
            ]
            self.energy_res = self.data_dict["scientific_metadata"]["RAW"][
                "energy_resolution"
            ]["value"]
            self.k_max = self.data_dict["scientific_metadata"]["RAW"]["k_max"]["value"]
            # self.noise = self.data_dict["scientific_metadata"]["RAW"]["noise"]["value"]
            self.edge_energy = self.data_dict["scientific_metadata"]["RAW"][
                "edge_energy"
            ]["value"]
            ## Store data:
            self.data_dict["scientific_metadata"]["Data"]["Energy"] = data.energy
            self.data_energy = self.data_dict["scientific_metadata"]["Data"]["Energy"]
            self.data_dict["scientific_metadata"]["Data"]["Mu"] = data.mu
            self.data_mu = self.data_dict["scientific_metadata"]["Data"]["Mu"]
            self.data_dict["scientific_metadata"]["Data"]["Flat"] = data.flat
            self.data_flat = self.data_dict["scientific_metadata"]["Data"]["Flat"]
            # Convert lists to JSON strings for storage
            energy_json = json.dumps(self.data_energy.tolist())
            mu_json = json.dumps(self.data_mu.tolist())
            flat_json = json.dumps(self.data_flat.tolist())

            if all(qc_list):
                print("DO SERVER COMMUNICATION -> CREATE DATASET")
                print("SENDING MESSAGE TO CURATOR...")
                send_mail(
                    "RefXAS: NEW DATASET CREATED",
                    "HEY MATE! \n\nSOMETHING EXCITING HAS HAPPENED: A NEW DATASET HAS BEEN CREATED! \nGO AND CURATE IT ASAP! \n\nSTAY HANDSOME :D"
                    + "\n\nPayload-preview:"
                    + "\n\nDATASET NAME:"
                    + str(self.data_set_name)
                    + "\n\nOWNER:"
                    + str(self.resp["owner"]),
                    EMAIL_HOST_USER,
                    [EMAIL_HOST_USER, "abhijeet.gaur@kit.edu"],
                    fail_silently=True,
                )
                update_dataset_dto = scicat_py.UpdateDatasetDto(
                    source_folder=self.short_url,
                    keywords=[
                        self.edge_step,
                        self.k_max,
                        self.energy_res,
                        self.edge_energy,
                        energy_json,
                        mu_json,
                        flat_json,
                    ],
                )  # UpdateDatasetDto |
                api_response = (
                    api_instance.datasets_controller_find_by_id_replace_or_create(
                        self.datasetId,
                        update_dataset_dto,
                        async_req=False,
                        _preload_content=False,
                    )
                )
                response = json.loads(api_response.data)
                self.data_dict["scientific_metadata"]["Figures"]["raw_data"]
                self.data_dict["scientific_metadata"]["Figures"]["normalized_data"]
                self.data_dict["scientific_metadata"]["Figures"]["k"]
                self.data_dict["scientific_metadata"]["Figures"]["R"]

    def upload_figure_data(self, figure: str, caption: Optional[str] = "") -> None:
        """
        Uploads a figure to the SciCat API as an attachment for a specific dataset.

        Args:
            figure (str): The figure data as a base64-encoded string.
            caption (str, optional): An optional caption for the figure attachment.

        Raises:
            ApiException: If there was an error while uploading the figure data.
        """
        QC_attach_figure_data = {
            "thumbnail": figure,
            "caption": caption,
            "access_groups": "None",
            "created_by": "string",
            "updated_by": "string",
            "owner_group": "some group",
        }
        with scicat_py.ApiClient(self.configuration) as api_client:
            api_client.configuration.access_token = self.access_token
            api_instance = scicat_py.DatasetsApi(api_client)
            create_attachment_dto = scicat_py.CreateAttachmentDto(
                **QC_attach_figure_data
            )
            api_response = api_instance.datasets_controller_create_attachment(
                self.datasetId,
                create_attachment_dto,
                async_req=False,
                _preload_content=False,
            )
            response = json.loads(api_response.data)
