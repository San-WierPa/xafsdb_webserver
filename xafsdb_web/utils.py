#import base64
#import urllib
#from io import BytesIO
from typing import Any

#import matplotlib.pyplot as plt
import scicat_py
#from PIL import Image

from ._auth_constants import CONFIGURATION, PASSWORD, USERNAME


def get_all_datasets() -> list:
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        dataset_meta_list = api_instance_dataset.datasets_controller_find_all()
    return dataset_meta_list


def term_checker(dataset: dict, term: str, array_accumulator: list) -> list:
    if term.lower() in dataset["datasetName"]:
        array_accumulator.append(dataset)


def get_access() -> str:
    """Returns cached access token"""
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        api_instance_auth = scicat_py.AuthApi(api_client)
        credentials_dto = scicat_py.CredentialsDto(username=USERNAME, password=PASSWORD)
        access_token = api_instance_auth.auth_controller_login(credentials_dto)[
            "access_token"
        ]
        return access_token


#def display_thumbnail(thumbnail: str) -> str:
#    """Returns string"""
#    img_thumbnail = Image.open(BytesIO(base64.b64decode(thumbnail)))
#    plt.imshow(img_thumbnail)
#    fig = plt.gcf()
#    buf = BytesIO()
#    fig.savefig(buf, format="png")
#    buf.seek(0)
#    string = base64.b64encode(buf.read())
#    return urllib.parse.quote(string)
