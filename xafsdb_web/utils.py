import scicat_py
from ._auth_constants import (USERNAME, PASSWORD, CONFIGURATION)

def get_all_datasets():
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token=access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        dataset_meta_list = api_instance_dataset.datasets_controller_find_all()
    return dataset_meta_list


def term_checker(dataset: dict, term: str, array_accumulator: list):
    if term.lower() in dataset["datasetName"]:
        array_accumulator.append(dataset)


def get_access():
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        api_instance_auth = scicat_py.AuthApi(api_client)
        credentials_dto = scicat_py.CredentialsDto(username=USERNAME, password=PASSWORD )
        access_token = api_instance_auth.auth_controller_login(credentials_dto)["access_token"]
        return access_token