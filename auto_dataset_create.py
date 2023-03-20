"""
@author: Sebastian Paripsa
"""

from __future__ import print_function
from pprint import pprint
import json
import os
from datetime import datetime
from sys import path
from typing import Optional
import environ
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
        print("data_set_name:", data_set_name)
        self.s3_data_path = s3_data_path
        print("s3_data_path:", s3_data_path)
        self.verify_data = verify_data

        print("Dataset creation initialized...how exciting!")
        print(
            "While you are waiting; why dont you go ahead and check out this awesome artist: https://open.spotify.com/artist/358PxMTt58AnnMo4tEFOVQ?si=qW1Oyl1LQzyfkFWvAVXEEA"
        )
        self.configuration = scicat_py.Configuration(
            host="http://35.233.84.253",
        )
        self.qc_path = "quality_control/"
        path.append(self.qc_path)
        self.auth_login()
        self.create_testdata()
        self.post_sthree()
        self.short_url()
        self.qc_and_update()
        self.upload_figure_data(figure=self.data_dict["scientific_metadata"]["Figures"]["raw_data"],
                                caption="Raw data")
        self.upload_figure_data(figure=self.data_dict["scientific_metadata"]["Figures"]["normalized_data"],
                                caption="Normalized data")
        self.upload_figure_data(figure=self.data_dict["scientific_metadata"]["Figures"]["k"],
                                caption="k")
        self.upload_figure_data(figure=self.data_dict["scientific_metadata"]["Figures"]["R"],
                                caption="R")

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
            # print(self.access_token)
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
            create_dataset_dto = scicat_py.CreateDatasetDto(**self.data_dict)
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
        print("I'm self.s3_data_path in post_sthree:", self.s3_data_path)
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
        #self.short_url = self.responds.json()["file"].split("?")[0]
        type_tiny = pyshorteners.Shortener()
        self.short_url = type_tiny.tinyurl.short(self.responds.json()["file"])
        #print(self.short_url)
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
            qc_list = [] ### this list will contain the quality criteria
            ### here the measurement data has to be forwarded, where will the data be stored in SciCat?
            meas_data = np.loadtxt(self.short_url, skiprows=1)
            #print("Meas_data from qc_and_update:", meas_data)
            cq.load_data(
                meas_data,
                source=self.data_dict["scientific_metadata"]["Source"],
                name=self.data_dict["dataset_name"],
            )
            ### perform preprocessing on the data
            data = cq.preprocess_data()
            ### plot the data and return the figure object
            fig_raw_data = cq.plot_raw_data()
            fig_normalized_data = cq.plot_normalized_data()
            fig_k = cq.plot_k()  ### plot data in k and return the figure object
            fig_R = cq.plot_R()  ### plot data in R and return the figure object
            self.data_dict["scientific_metadata"]["Figures"]["raw_data"] = cq.encode_base64_figure(fig_raw_data)
            self.data_dict["scientific_metadata"]["Figures"]["normalized_data"] = cq.encode_base64_figure(fig_normalized_data)
            self.data_dict["scientific_metadata"]["Figures"]["k"] = cq.encode_base64_figure(fig_k)
            self.data_dict["scientific_metadata"]["Figures"]["R"] = cq.encode_base64_figure(fig_R)
            ### check for the edge step
            qc_list.append(cq.check_edge_step())
            ### add to dummy data
            self.data_dict["scientific_metadata"]["RAW"]["edge_step"]["value"] = qc_list[0][1]
            ### check for the energy resolution
            qc_list.append(cq.check_energy_resolution())
            ### add to dummy data
            self.data_dict["scientific_metadata"]["RAW"]["energy_resolution"]["value"] = qc_list[1][1]
            ### check for k
            qc_list.append(cq.check_k())
            ### add to dummy data
            self.data_dict["scientific_metadata"]["RAW"]["k_max"]["value"] = qc_list[2][1]
            ### Hand over quality criteria to webserver
            self.edge_step = self.data_dict["scientific_metadata"]["RAW"]["edge_step"]["value"]
            self.energy_res = self.data_dict["scientific_metadata"]["RAW"]["energy_resolution"]["value"]
            self.k_max = self.data_dict["scientific_metadata"]["RAW"]["k_max"]["value"]
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
                self.data_dict["scientific_metadata"]["Figures"]["raw_data"]
                #pprint(self.raw_data_fig)
                self.data_dict["scientific_metadata"]["Figures"]["normalized_data"]
                self.data_dict["scientific_metadata"]["Figures"]["k"]
                self.data_dict["scientific_metadata"]["Figures"]["R"]

    def upload_figure_data(self, figure, caption=""):
        """
        QC attachment -> Upload main data
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
            create_attachment_dto = scicat_py.CreateAttachmentDto(**QC_attach_figure_data)
            api_response = api_instance.datasets_controller_create_attachment(
                self.datasetId,
                create_attachment_dto,
                async_req=False,
                _preload_content=False,
            )
            response = json.loads(api_response.data)
            # pprint(response)
