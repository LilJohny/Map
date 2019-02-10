import pandas
import re
from entities import Episode, Film
from pathlib import Path
from location_utils import strip_location
import os
import pickle


def create_file_generator(file_path):
    '''Function acts like generator for file reading
    
    Arguments:
        file_path {str} -- filepath
    '''

    with open(file_path, 'r') as file:
        for row in file:
            yield row


def filter_valid_locations(base):
    '''Function filter database and returns films with known coordinates
    
    Arguments:
        base {list} -- database
    
    Returns:
        list -- filtered database
    '''

    file_path = os.sep.join([str(Path(os.getcwd()).parent), 'static_files', 'dictionary_coordinates.bin'])
    coordinates = pickle.load(open(file_path, 'rb'))
    base = list(map(lambda x: (x[0], x[1], x[2], strip_location(x[3])), base))
    base = list(filter(
        lambda x: x[-1] is not None and coordinates.get(x[-1]) is not None and coordinates[x[-1]] is not None, base))
    return base


def select_year(base: list, year: int):
    '''Function filter given database and returns database for particular year
    
    Arguments:
        base {list} -- database
        year {int} -- year
    
    Returns:
        list -- filtered database
    '''

    base = list(filter(lambda x: x[1].count(str(year)) == 1, base))
    return base


def select_country(base, country):
    '''Function filter given database and returns database for particular country
    
    Arguments:
        base {list} --  database list
        country {str} --  country
    
    Returns:
        list -- filtered database
    '''

    base = list(filter(lambda x: x[-1].count(country) == 1, base))
    return base


def convert_to_list(base):
    '''Function converts database from DataFrame to list
    
    Arguments:
        base {pandas.DataFrame} -- base to convert
    
    Returns:
        list -- converted base
    '''

    movie_cl = base['movie'].values.tolist()
    year_cl = base['year'].values.tolist()
    add_info_cl = base['add_info'].values.tolist()
    locations_cl = base['location'].values.tolist()
    converted_base = list(zip(movie_cl, year_cl, add_info_cl, locations_cl))
    return converted_base


def read_database_from_csv(file_name):
    '''Function reads database from .csv file
    
    Arguments:
        file_name {str} -- Database file name
    
    Returns:
        pandas.DataFrame -- database DataFrame
    '''

    base_df = pandas.read_csv(file_name, sep=',', error_bad_lines=False, encoding='utf-8', lineterminator='\n')
    if any(map(lambda x: x.count('\r') != 0, list(base_df.keys()))):
        base_df = base_df.rename(index=str, columns={key: key.replace('\r', '') for key in list(base_df.keys())})
    return base_df


def read_database_from_list(file_name):
    '''Function reads database from .list file
    
    Arguments:
        file_name {str} -- database file to read from
    
    Returns:
        list -- list of rows from file
    '''

    rows = []
    file_generator = create_file_generator(file_name)
    for _ in range(14):
        next(file_generator)
    for row in file_generator:
        if row.count('(????') == 0:
            rows.append(row)
    del rows[-1]
    del rows[-2]

    return rows


def strip_title(title):
    '''Function strips title to normal form
    
    Arguments:
        title {str} -- title to strip
    
    Returns:
        str -- stripped title
    '''

    title = title.replace('#', '')
    title = title.replace('"', '')
    title = title.strip()
    return title


def transform(base):
    '''This function transforms base, read from .list file to normal form
    
    Arguments:
        base {list} -- list of rows from file 
    
    Returns:
        list -- Transfromed base(list of tuples)
    '''

    transformed_base = []
    for row in base:
        is_episode = False
        row = row.strip()
        year = re.search(r'(?<!\d)\((\d{4})(?!\d)', row)[0].replace('(', '')
        year = int(year)
        year_to_replace = re.search(r'(?<!\d)(\(\d{4}/*\w*\))(?!\d)', row)[0]
        row = row.replace(year_to_replace, '')
        episode = re.search(r'(?<!\d)({.*\(#\d.\d\)})(?!\d)', row)
        if not (episode is None):
            is_episode = True
            row = row.replace(episode[0], '')
            episode = episode[0].replace('{', '').replace('}', '')
        row = list(filter(lambda x: x != '', row.split('\t')))
        title, location = strip_title(row[0]), row[1]
        if is_episode:
            episode = Episode(title_name=title, episode_name=episode, location=location, year=year, coordinates=None)
            transformed_base.append(episode)
        else:
            film = Film(title_name=title, location=location, year=year, coordinates=None)
            transformed_base.append(film)
    return transformed_base
