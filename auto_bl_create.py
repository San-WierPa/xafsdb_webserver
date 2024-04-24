"""
auto_bl_create.py
-----------------------
@author: Sebastian Paripsa
@email: paripsa@uni-wuppertal.de (or: sebastian.paripsa@gmail.com)
@linkedin: https://www.linkedin.com/in/sebastian-paripsa/
@git: https://github.com/San-WierPa
@orcid: https://orcid.org/0009-0000-3487-5399

Description:
------------
This script automates the process of Beamline creation by using the SciCat API.
It performs data reading and uploads the Beamline to the designated repository.

SEO Tags:
---------
#SciCat #DatasetAutomation #Python #DataScience

Modules:
--------
-

Requirements:
-------------
- Python 3.10
- SciCat API access

"""

from __future__ import print_function

import json
import random
import string
from typing import Optional

import environ

import scicat_py

env = environ.Env()
environ.Env.read_env()
prefix = env("PREFIX")


class AutoBlCreation(object):
    """
    This class automatically creates a Beamline,
    and serves all to the webserver
    """

    def __init__(self, verify_beamline_meta) -> None:
        self.configuration = scicat_py.Configuration(
            # production
            host="http://34.29.91.220",
            # dev (varies due to shut-down/restart of vm - every restart changes ip)
            # host="http://34.29.27.51",
        )
        self.auth_login()
        self.verify_beamline_meta = verify_beamline_meta
        self.create_beamline()
        self.generate_random_string()

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

    def generate_random_string(self):
        # Get all the ASCII letters in lowercase and uppercase
        letters = string.ascii_letters
        # Randomly choose characters from letters for the given length of the string
        self.random_str = "".join(random.choice(letters) for i in range(15))
        return self.random_str

    def create_beamline(self) -> Optional[str]:
        """
        Creates a new beamline and returns its ID.

        Returns:
            str or None: The ID of the created beamline or None if an error occurred.
        """
        print("In the dic")
        self.beamline_dict = {
            "name": "PID.BEAMLINE.PREFIX." + self.generate_random_string(),
            "custom_metadata": {
                "SOURCE": self.verify_beamline_meta.get("Source"),
                "FACILITY": {
                    "synchrotronName": self.verify_beamline_meta.get("synchrotronName"),
                    "beamline": self.verify_beamline_meta.get("beamline"),
                },
                "STORAGE_RING": {
                    "elektronEnergy": self.verify_beamline_meta.get("elektronEnergy"),
                    "elektronBeamEmittance": self.verify_beamline_meta.get(
                        "elektronBeamEmittance"
                    ),
                    "fillingMode": self.verify_beamline_meta.get("fillingMode"),
                },
                "MIRRORS": {
                    "use_mirror": self.verify_beamline_meta.get("use_mirror"),
                    "mirrortype": self.verify_beamline_meta.get("mirrortype"),
                    "mirrorposition": self.verify_beamline_meta.get("mirrorposition"),
                    "reflectingmaterial": self.verify_beamline_meta.get(
                        "reflectingmaterial"
                    ),
                    "angleofincidence": self.verify_beamline_meta.get(
                        "angleofincidence"
                    ),
                },
                "FILTERS_WINDOWS": {
                    "filter": self.verify_beamline_meta.get("filter"),
                    "windows": self.verify_beamline_meta.get("windows"),
                },
                "DETECTORS": {
                    "detectorsI0": self.verify_beamline_meta.get("detectorsI0"),
                    "detectorsI1": self.verify_beamline_meta.get("detectorsI1"),
                    "detectorsfluo": self.verify_beamline_meta.get("detectorsfluo"),
                },
                "SCANPARAM": {
                    "detectionmode": self.verify_beamline_meta.get("detectionmode"),
                    "scanmode": self.verify_beamline_meta.get("scanmode"),
                    "monochromatic": self.verify_beamline_meta.get("monochromatic"),
                    "beamsize": self.verify_beamline_meta.get("beamsize"),
                    "higherharmonic": self.verify_beamline_meta.get("higherharmonic"),
                },
                "SOURCETYPE": {
                    "sourcetype": self.verify_beamline_meta.get("sourcetype"),
                    "criticalEnergy": self.verify_beamline_meta.get("criticalEnergy"),
                    "maximumKvalue": self.verify_beamline_meta.get("maximumKvalue"),
                },
                "MONOCHROMATOR": {
                    "type": self.verify_beamline_meta.get("type"),
                    "CRYSTALS": {
                        "channelcut": self.verify_beamline_meta.get("channelcut"),
                        "fixedexit": self.verify_beamline_meta.get("fixedexit"),
                    },
                    "latticespacing": self.verify_beamline_meta.get("latticespacing"),
                    "temperature_of_crystals": self.verify_beamline_meta.get(
                        "temperature_of_crystals"
                    ),
                    "sourceDCM": self.verify_beamline_meta.get("sourceDCM"),
                    "DCMsample": self.verify_beamline_meta.get("DCMsample"),
                    "encoder_theta": self.verify_beamline_meta.get("encoder_theta"),
                    "position_slits": self.verify_beamline_meta.get("position_slits"),
                    "opening_slits": self.verify_beamline_meta.get("opening_slits"),
                    "energyresolution_edge": self.verify_beamline_meta.get(
                        "energyresolution_edge"
                    ),
                    "detuning": self.verify_beamline_meta.get("detuning"),
                },
                "BEAMDAMAGE": {
                    "use_beamdamage": self.verify_beamline_meta.get("use_beamdamage"),
                    "beamdamagetype": self.verify_beamline_meta.get("beamdamagetype"),
                },
                "CONTACT": {
                    "bl_author": self.verify_beamline_meta.get("bl_author"),
                    "bl_institute": self.verify_beamline_meta.get("bl_institute"),
                    "bl_author_mail": self.verify_beamline_meta.get("bl_author_mail"),
                },
            },
        }

        with scicat_py.ApiClient(self.configuration) as api_client:
            api_client.configuration.access_token = self.access_token
            api_instance = scicat_py.InstrumentsApi(api_client)
            # print("api_instance:", api_instance)
            create_instrument_dto = scicat_py.CreateInstrumentDto(**self.beamline_dict)
            api_response = api_instance.instruments_controller_create(
                create_instrument_dto, async_req=False, _preload_content=False
            )
            resp = json.loads(api_response.data)
            self.beamlineId = resp["id"]
            print("ME BEAMLINE ID:", self.beamlineId)
            return self.beamlineId
