"""
utils.py
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

import scicat_py

from ._auth_constants import CONFIGURATION, PASSWORD, USERNAME

def get_access() -> str:
    """Returns cached access token"""
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        api_instance_auth = scicat_py.AuthApi(api_client)
        credentials_dto = scicat_py.CredentialsDto(username=USERNAME, password=PASSWORD)
        access_token = api_instance_auth.auth_controller_login(credentials_dto)[
            "access_token"
        ]
        return access_token


def get_all_datasets() -> list:
    """
    Retrieves a list of all dataset metadata from the configured SciCat instance.

    This function initializes an API client using the specified global configuration,
    authenticates with the SciCat server to obtain an access token, and then
    queries the SciCat Datasets API to fetch metadata for all available datasets.

    The function handles the authentication process internally and assumes that
    the global configuration (`CONFIGURATION`) and the method to obtain an access
    token (`get_access()`) are defined and accessible in the current scope.

    Returns:
        list: A list of dictionaries, where each dictionary contains metadata
        for a single dataset. The specific structure of each dictionary is
        determined by the SciCat Datasets API response format.

    Note:
        This function depends on the `scicat_py` package for interacting with
        the SciCat API. Ensure that this package is installed and properly
        configured in your environment.

    Raises:
        Various exceptions can be raised by the underlying `scicat_py.ApiClient`
        and `scicat_py.DatasetsApi` methods, depending on the nature of the failure
        (e.g., network issues, authentication failures, API changes). It is
        recommended to handle exceptions at the call site of this function.
    """
    with scicat_py.ApiClient(configuration=CONFIGURATION) as api_client:
        access_token = get_access()
        api_client.configuration.access_token = access_token

        api_instance_dataset = scicat_py.DatasetsApi(api_client)
        dataset_meta_list = api_instance_dataset.datasets_controller_find_all()
    return dataset_meta_list


def term_checker(dataset: dict, term: str, datasetList: list) -> None:
    term_found = False

    if term.lower() in dataset['datasetName'].lower():
        term_found = True
    elif term.lower() in str(dataset.get('ownerGroup', '')).lower():
        term_found = True
    elif term.lower() in str(dataset.get('owner', '')).lower():
        term_found = True
    elif term.lower() in str(dataset.get('contactEmail', '')).lower():
        term_found = True
    else:
        for key, value in dataset['scientificMetadata'].items():
            if term_found:
                break
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if term.lower() in str(sub_value).lower():
                        term_found = True
                        break
            else:
                if term.lower() in str(value).lower():
                    term_found = True

    if term_found:
        datasetList.append(dataset)

def snake_case_to_title_case(snake_str):
    # Split the string by underscore, capitalize each part, and join with spaces
    return ' '.join(word.capitalize() for word in snake_str.split('_'))