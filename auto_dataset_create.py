"""
@author: Sebastian Paripsa
"""

from __future__ import print_function

import json
import os
from datetime import datetime
from sys import path

# from scicat_py.rest import ApiException
import numpy as np
import pyshorteners
import requests
import scicat_py

# from pprint import pprint
from quality_control.quality_check import check_quality


class AutoDatasetCreation(object):
    """
    This class automatically creates a dataset, does the quality_control
    and serves all to the webserver
    """

    def __init__(self):
        print("Dataset creation initialized...how exciting!")
        print(
            "While you are waiting; why dont you go ahead and check out this awesome artist: https://open.spotify.com/artist/358PxMTt58AnnMo4tEFOVQ?si=qW1Oyl1LQzyfkFWvAVXEEA"
        )
        self.configuration = scicat_py.Configuration(
            host="http://35.233.84.253",
        )
        self.qc_path = "quality_control/"  # "quality_control/"  # "/app/"
        path.append(self.qc_path)
        self.auth_login()
        self.create_testdata()
        self.post_sthree()
        self.short_url()
        self.qc_and_update()
        self.upload_data()
        self.upload_k()
        self.upload_R()

    def auth_login(self) -> str:
        """
        Verify access
        """
        with scicat_py.ApiClient(configuration=self.configuration) as api_client:
            api_instance = scicat_py.AuthApi(api_client)
            credentials_dto = scicat_py.CredentialsDto(
                username=os.environ["USERNAME_AUTH"],
                password=os.environ["PASSWORD_AUTH"],
            )
            api_response = api_instance.auth_controller_login(credentials_dto)
            self.access_token = api_response["access_token"]
            # print(self.access_token)
            return self.access_token

    def create_testdata(self):
        """
        Create dataset with quality_control data
        """
        titlename = input("Enter name of dataset title: ")
        self.dummy_data2 = {
            "owner_group": "University of Wuppertal",
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
            "owner": "None",
            "contact_email": "a@b.de",
            "scientific_metadata": {
                "Abstract": "This is a very descriptive and long informative abstract to understand this dataset a bit better!",
                "Source": "LABORATORY",
                "Mode": "ABSORPTION",
                "RAW": {
                    "edge_step": {
                        "value": 0.0,
                        "unit": "1",
                        "documentation": "height of the detected edge step",
                    },
                    "k_max": {
                        "value": 0.0,
                        "unit": "1/angstrom",
                        "documentation": "considered angular wavenumber",
                    },
                    "noise": {
                        "value": 0.0,
                        "unit": "1",
                        "documentation": "noise of the measurement",
                    },
                    "energy_resolution": {
                        "value": 0.0,
                        "unit": "eV",
                        "documentation": "energy resolution of the measured spectrum in eV",
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
                        "unit": "1",
                        "documentation": "amplitude factor from the processed spectrum",
                    }
                },
                "Figures": {
                    "data": None,
                    "k": None,
                    "R": None,
                },
            },
        }

        with scicat_py.ApiClient(self.configuration) as api_client:
            api_client.configuration.access_token = self.access_token
            api_instance = scicat_py.DatasetsApi(api_client)
            create_dataset_dto = scicat_py.CreateDatasetDto(**self.dummy_data2)
            api_response = api_instance.datasets_controller_create(
                create_dataset_dto, async_req=False, _preload_content=False
            )
            resp = json.loads(api_response.data)
            self.datasetId = resp["id"]
            # print(self.datasetId)
            return self.datasetId

    def post_sthree(self):
        """
        Post to S3 amazon object storage
        """
        filename = input("Enter name of input file: ")
        files = {
            "file": open(self.qc_path + "example data/LABORATORY/" + filename, "rb")
        }
        values = {"dataset_id": self.datasetId}
        self.responds = requests.post(
            "http://35.233.84.253/file/file/", files=files, data=values
        )
        # print(self.responds.json())
        return self.responds

    def short_url(self):
        """
        Helper function to shorten the s3 amazon url

        TODO: creates folder and downloads the file -> should not do it
        """
        type_tiny = pyshorteners.Shortener()
        self.short_url = type_tiny.tinyurl.short(self.responds.json()["file"])
        # print(self.short_url)
        return self.short_url

    def qc_and_update(self):
        """
        Main function for quality_control
        """
        with scicat_py.ApiClient(self.configuration) as api_client:
            api_client.configuration.access_token = self.access_token
            api_instance = scicat_py.DatasetsApi(api_client)

            ## CHECK QUALITY CONTROL ->

            cq_json = (
                self.qc_path + "Criteria.json"
            )  ### loading the json criteria file for reference
            cq = check_quality(
                quality_criteria_json=cq_json
            )  ### initialize quality check object
            qc_list = []  ### this list will contain the quality criteria
            meas_data = np.loadtxt(
                self.short_url, skiprows=1
            )  ### here the measurement data has to be forwarded, where will the data be stored in SciCat?
            cq.load_data(
                meas_data,
                source=self.dummy_data2["scientific_metadata"]["Source"],
                name=self.dummy_data2["dataset_name"],
            )
            data = cq.preprocess_data()  ### perform preprocessing on the data
            fig_data = (
                cq.plot_background()
            )  ### plot the data and return the figure object
            fig_k = cq.plot_k()  ### plot data in k and return the figure object
            fig_R = cq.plot_R()  ### plot data in R and return the figure object
            self.dummy_data2["scientific_metadata"]["Figures"][
                "data"
            ] = cq.encode_base64_figure(fig_data)
            self.dummy_data2["scientific_metadata"]["Figures"][
                "k"
            ] = cq.encode_base64_figure(fig_k)
            self.dummy_data2["scientific_metadata"]["Figures"][
                "R"
            ] = cq.encode_base64_figure(fig_R)
            qc_list.append(cq.check_edge_step())  ### check for the edge step
            self.dummy_data2["scientific_metadata"]["RAW"]["edge_step"][
                "value"
            ] = qc_list[0][
                1
            ]  ### add to dummy data
            qc_list.append(
                cq.check_energy_resolution()
            )  ### check for the energy resolution
            self.dummy_data2["scientific_metadata"]["RAW"]["energy_resolution"][
                "value"
            ] = qc_list[1][
                1
            ]  ### add to dummy data
            qc_list.append(cq.check_k())
            self.dummy_data2["scientific_metadata"]["RAW"]["k_max"]["value"] = qc_list[
                2
            ][
                1
            ]  ### add to dummy data
            # print(dummy_data2)
            if all(qc_list):
                print("DO SERVER COMMUNICATION -> CREATE DATASET")
                update_dataset_dto = scicat_py.UpdateDatasetDto(
                    source_folder=self.short_url
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
                # pprint(response)
                self.data_fig = self.dummy_data2["scientific_metadata"]["Figures"][
                    "data"
                ]
                self.k_fig = self.dummy_data2["scientific_metadata"]["Figures"]["k"]
                self.R_fig = self.dummy_data2["scientific_metadata"]["Figures"]["R"]

    def upload_data(self):
        """
        QC attachment -> Upload main data
        """
        QC_attach_data = {
            "thumbnail": self.data_fig,
            "caption": "some caption",
            "access_groups": "None",
            "created_by": "string",
            "updated_by": "string",
            "owner_group": "some group",
        }
        with scicat_py.ApiClient(self.configuration) as api_client:
            api_client.configuration.access_token = self.access_token
            api_instance = scicat_py.DatasetsApi(api_client)
            create_attachment_dto = scicat_py.CreateAttachmentDto(**QC_attach_data)
            api_response = api_instance.datasets_controller_create_attachment(
                self.datasetId,
                create_attachment_dto,
                async_req=False,
                _preload_content=False,
            )
            response = json.loads(api_response.data)
            # pprint(response)

    def upload_k(self):
        """
        QC attachment -> Upload k
        """
        QC_attach_k = {
            "thumbnail": self.k_fig,
            "caption": "some caption",
            "access_groups": "None",
            "created_by": "string",
            "updated_by": "string",
            "owner_group": "some group",
        }
        with scicat_py.ApiClient(self.configuration) as api_client:
            api_client.configuration.access_token = self.access_token
            api_instance = scicat_py.DatasetsApi(api_client)
            create_attachment_dto = scicat_py.CreateAttachmentDto(**QC_attach_k)
            api_response = api_instance.datasets_controller_create_attachment(
                self.datasetId,
                create_attachment_dto,
                async_req=False,
                _preload_content=False,
            )
            response = json.loads(api_response.data)
            # pprint(response)

    def upload_R(self):
        """
        QC attachment -> Upload R
        """
        QC_attach_R = {
            "thumbnail": self.R_fig,
            "caption": "some caption",
            "access_groups": "None",
            "created_by": "string",
            "updated_by": "string",
            "owner_group": "some group",
        }
        with scicat_py.ApiClient(self.configuration) as api_client:
            api_client.configuration.access_token = self.access_token
            api_instance = scicat_py.DatasetsApi(api_client)
            create_attachment_dto = scicat_py.CreateAttachmentDto(**QC_attach_R)
            api_response = api_instance.datasets_controller_create_attachment(
                self.datasetId,
                create_attachment_dto,
                async_req=False,
                _preload_content=False,
            )  #
            response = json.loads(api_response.data)
            # pprint(response)
            print("ALL DONE!")


var = AutoDatasetCreation()
