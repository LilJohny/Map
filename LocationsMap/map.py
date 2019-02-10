import folium
import os
from location_utils import get_coordinates
from pathlib import Path
import os
from data_utils import read_database_from_csv, convert_to_list, select_year, select_country, filter_valid_locations


def get_color(population):
    '''This function returns color for given population
    
    Arguments:
        population {int} -- population in zone
    
    Returns:
        str -- color for given population
    '''

    if population < 2000:
        return "green"
    elif 2000 <= population <= 3500:
        return "yellow"
    else:
        return "red"


def create_map(condition_type, condition, map_file,  limit):
    '''This function creates map and saves it to file with given name.
    
    Arguments:
        condition_type {int } -- 1 if map should be build for year and 2 for country.
        condition {int or str} -- year or country.
        map_file {str} -- name for map file to save.
        limit {int or None} -- number of markers to display if their number is limited else None.
    '''

    base_file = os.sep.join(
        [str(Path(os.getcwd()).parent), 'static_files', 'locations.csv'])
    base = convert_to_list(read_database_from_csv(base_file))

    if condition_type == 1:
        base = select_year(base, condition)
    elif condition_type == 2:
        base = select_country(base, condition)

    base = filter_valid_locations(base)
    if limit is not None:
        base = base[:limit]
    locations = list(map(lambda x: x[-1], base))
    titles = list(map(lambda x: x[0], base))
    add_info = list(map(lambda x: x[2], base))
    add_info = list(map(lambda x: x.replace(
        '{', '').replace('}', '').replace('NO DATA', ''), add_info))
    coordinates = get_coordinates(locations)
    locations_map = folium.Map(zoom_start=10)

    populations_file = os.sep.join(
        [str(Path(os.getcwd()).parent), 'static_files', 'world.json'])
    second_layer = folium.FeatureGroup(name='Population')
    second_layer.add_child(
        folium.GeoJson(data=open(populations_file, 'r', encoding='utf-8-sig').read(),
                       style_function=lambda x: {'fillColor': 'green'
                                                 if x['properties']['POP2005'] < 10000000
                                                 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                 else 'red'}))
    locations_features = folium.FeatureGroup(name='Films')

    for [lt, ln], title, add_info, in list(zip(coordinates, titles, add_info)):
        locations_features.add_child(
            folium.Marker(location=[lt, ln], popup='\n'.join([title, add_info]),
                          icon=folium.Icon()))
    locations_map.add_child(second_layer)
    locations_map.add_child(locations_features)
    locations_map.add_child(folium.LayerControl())
    if not os.path.exists(os.sep.join([str(Path(os.getcwd()).parent), 'Maps'])):
        os.mkdir(os.sep.join([str(Path(os.getcwd()).parent), 'Maps']))
    save_path = os.sep.join([str(Path(os.getcwd()).parent), 'Maps', map_file])
    locations_map.save(save_path)
