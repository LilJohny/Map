import pickle
import string
import os
from pathlib import Path


def strip_location(location):
    location = list(filter(lambda x: all([var in string.ascii_letters for var in x]), location.split(' ')))
    return ' '.join(location)


def get_coordinates(locations: list):
    file_path = os.sep.join([str(Path(os.getcwd()).parent), 'static_files', 'dictionary_coordinates.bin'])
    coordinates = pickle.load(open(file_path, 'rb'))
    coordinates_list = [coordinates[location] for location in locations]
    return coordinates_list
