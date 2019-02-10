import pickle
import string
import os
from pathlib import Path


def strip_location(location):
    '''Function strips locatio to normal form
    
    Arguments:
        location {str} -- location to strip
    
    Returns:
        str -- stripped location
    '''

    location = list(filter(lambda x: all([var in string.ascii_letters for var in x]), location.split(' ')))
    return ' '.join(location)


def get_coordinates(locations: list):
    '''Function returns list of coordinates for given list of locations
    
    Arguments:
        locations {list} -- locations
    
    Returns:
        list -- coordinates
    '''

    file_path = os.sep.join([str(Path(os.getcwd()).parent), 'static_files', 'dictionary_coordinates.bin'])
    coordinates = pickle.load(open(file_path, 'rb'))
    coordinates_list = [coordinates[location] for location in locations]
    return coordinates_list
