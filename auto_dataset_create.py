"""
@author: Sebastian Paripsa
"""

from __future__ import print_function

import json
import os
from datetime import datetime
from sys import path

import environ
# from scicat_py.rest import ApiException
import numpy as np
import pyshorteners
import requests
import scicat_py
# from pprint import pprint
from quality_control.quality_check import check_quality

env = environ.Env()
environ.Env.read_env()


class AutoDatasetCreation(object):
    """
    This class automatically creates a dataset, does the quality_control
    and serves all to the webserver
    """

    def __init__(self, s3_data_path, data_set_name, verify_data):
        self.data_set_name = data_set_name
        self.s3_data_path = s3_data_path
        self.verify_data = verify_data

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
                # username=os.environ["USERNAME_AUTH"],
                # password=os.environ["PASSWORD_AUTH"],
                username=env("USERNAME_AUTH"),
                password=env("PASSWORD_AUTH"),
            )
            api_response = api_instance.auth_controller_login(credentials_dto)
            self.access_token = api_response["access_token"]
            # print(self.access_token)
            return self.access_token

    def create_testdata(self):
        """
        Create dataset with quality_control data
        """
        titlename = self.data_set_name
        self.dummy_data2 = {
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
                "Abstract": self.verify_data.get("Abstract"),
                "Source": self.verify_data.get("Source"),
                "Mode": self.verify_data.get("Measurement Mode"),
                "RAW": {
                    "edge_step": {
                        "value": 0.0,
                        "unit": "a.u.",
                        "documentation": "Height of the detected edge step.",
                    },
                    "k_max": {
                        "value": 0.0,
                        "unit": "1/angstrom",
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
                    "data": None, #TODO data -> absorbance
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
                },
            },
            "keywords": "None",
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
        files = {"file": open(self.s3_data_path, "rb")}
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

            ### CHECK QUALITY CONTROL ###
            ### loading the json criteria file for reference
            cq_json = (self.qc_path + "Criteria.json")
            ### initialize quality check object
            cq = check_quality(quality_criteria_json=cq_json)  
            qc_list = []  ### this list will contain the quality criteria
            ### here the measurement data has to be forwarded, where will the data be stored in SciCat?
            meas_data = np.loadtxt(self.short_url, skiprows=1)  
            cq.load_data(meas_data,
                         source=self.dummy_data2["scientific_metadata"]["Source"],
                         name=self.dummy_data2["dataset_name"],)
            ### perform preprocessing on the data
            data = cq.preprocess_data() 
            ### plot the data and return the figure object
            fig_raw_data = (cq.plot_raw_data())
            fig_normalized_data = (cq.plot_normalized_data())
            fig_k = cq.plot_k()  ### plot data in k and return the figure object
            fig_R = cq.plot_R()  ### plot data in R and return the figure object
            self.dummy_data2["scientific_metadata"]["Figures"
                                                    ]["raw data"] = cq.encode_base64_figure(fig_raw_data)
            self.dummy_data2["scientific_metadata"]["Figures"
                                                    ]["normalized data"] = cq.encode_base64_figure(fig_normalized_data)
            self.dummy_data2["scientific_metadata"]["Figures"]["k"
                                                               ] = cq.encode_base64_figure(fig_k)
            self.dummy_data2["scientific_metadata"]["Figures"]["R"
                                                               ] = cq.encode_base64_figure(fig_R)
            ### check for the edge step
            qc_list.append(cq.check_edge_step())  
            ### add to dummy data
            self.dummy_data2["scientific_metadata"]["RAW"]["edge_step"]["value"
                                                                        ] = qc_list[0][1]  
            ### check for the energy resolution
            qc_list.append(cq.check_energy_resolution())  
            ### add to dummy data
            self.dummy_data2["scientific_metadata"]["RAW"]["energy_resolution"][
                "value"] = qc_list[1][1]
            qc_list.append(cq.check_k())
            self.dummy_data2["scientific_metadata"]["RAW"]["k_max"]["value"] = qc_list[
                2
            ][
                1
            ]  ### add to dummy data
            self.edge_step = self.dummy_data2["scientific_metadata"]["RAW"]["edge_step"]["value"]
            self.energy_res = self.dummy_data2["scientific_metadata"]["RAW"]["energy_resolution"]["value"]
            self.k_max = self.dummy_data2["scientific_metadata"]["RAW"]["k_max"]["value"]
            # print(dummy_data2)
            if all(qc_list):
                print("DO SERVER COMMUNICATION -> CREATE DATASET")
                update_dataset_dto = scicat_py.UpdateDatasetDto(
                    source_folder=self.short_url,
                    keywords=[self.edge_step, self.k_max, self.energy_res],
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
                self.raw_data_fig = self.dummy_data2["scientific_metadata"]["Figures"]["raw data"]
                self.normalized_data_fig = self.dummy_data2["scientific_metadata"]["Figures"]["normalized data"]
                self.k_fig = self.dummy_data2["scientific_metadata"]["Figures"]["k"]
                self.R_fig = self.dummy_data2["scientific_metadata"]["Figures"]["R"]

    def upload_raw_data(self):
        """
        QC attachment -> Upload main data
        """
        QC_attach_data = {
            "thumbnail": self.raw_data_fig,
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
            
    def upload_normalized_data(self):
        """
        QC attachment -> Upload main data
        """
        QC_attach_data = {
            "thumbnail": self.normalized_data_fig,
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
