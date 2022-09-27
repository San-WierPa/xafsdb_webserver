import requests


def get_all_datasets():
    url = f"http://127.0.0.1:8000/api/v1/dataset/list"
    response = requests.get(url)
    datasetList = response.json()
    return datasetList


def term_checker(dataset: dict, term: str, array_accumulator: list):
    if term.lower() in dataset["title"]:
        array_accumulator.append(dataset)
