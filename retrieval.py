import json


def load_dataset():

    with open("dataset.json", "r") as file:

        dataset = json.load(file)

    return dataset