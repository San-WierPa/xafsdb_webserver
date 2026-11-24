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
    """
    Check if a given term is present in either the updated metadata within a dataset's history
    or in its current scientific metadata and append it to a list if found.

    Args:
        dataset (dict): A dictionary representing a dataset which might contain both current
                        and historically updated metadata.
        term (str): The search term used to filter datasets based on their metadata content.
        datasetList (list): A list to which datasets matching the search term are appended.

    Details:
        The function first checks for the term within the dataset's historical metadata ('history'),
        looking specifically at any 'updatedscientificMetadata'. If the term is found in any of
        the historical entries, the check halts, and the dataset is added to the list, prioritizing
        the most recent data.

        If the term is not found in the historical updates, the function falls back to the dataset's
        current 'scientificMetadata'. It searches through all fields, including nested dictionaries,
        for the term.

        If the term still isn't found after checking historical and current metadata, the function
        performs a final check against other top-level fields such as 'datasetName', 'ownerGroup',
        'owner', 'contactEmail', and 'updatedBy'.

        The dataset is only added to the provided list if the term is found in any of the checked locations.

    Process:
        1. Iterate over each history entry and check if 'updatedscientificMetadata' contains the term.
        2. If not found, check the current 'scientificMetadata'.
        3. If still not found, check additional specified top-level fields.
        4. Append the dataset to 'datasetList' if any of the checks are positive.
    """
    term_found = False
    term_lower = term.lower()

    # Check if there are updates in the history
    history = dataset.get("history", [])
    for history_entry in history:
        updated_metadata = history_entry.get("updatedscientificMetadata", {})
        for key, value in updated_metadata.items():
            if isinstance(value, dict):
                # Check each value inside the nested dictionary
                if any(
                    term_lower in str(sub_value).lower() for sub_value in value.values()
                ):
                    term_found = True
                    break
            elif term_lower in str(value).lower():
                term_found = True
                break
        if term_found:
            break

    # Fallback to checking current scientificMetadata if no term is found in history
    if not term_found:
        for key, value in dataset["scientificMetadata"].items():
            if isinstance(value, dict):
                if any(
                    term_lower in str(sub_value).lower() for sub_value in value.values()
                ):
                    term_found = True
                    break
            elif term_lower in str(value).lower():
                term_found = True
                break

    # Additional top-level fields checks (if needed)
    if not term_found:
        if any(
            term_lower in dataset.get(field, "").lower()
            for field in [
                "datasetName",
                "ownerGroup",
                "owner",
                "contactEmail",
                "updatedBy",
            ]
        ):
            term_found = True

    if term_found:
        datasetList.append(dataset)


def snake_case_to_title_case(snake_str):
    # Split the string by underscore, capitalize each part, and join with spaces
    return " ".join(word.capitalize() for word in snake_str.split("_"))
