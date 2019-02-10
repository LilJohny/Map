import geocoder
import pickle


def load_rest(file):
    '''Function returns generator for given file
    
    Arguments:
        file {str} -- File name to load
    
    Returns:
        list -- loaded file
    '''

    return pickle.load(open(file, 'rb'))


def geocode(locations_file_name, rest_file_name):
    '''Function performs geocoding and saves results to file with given name
    
    Arguments:
        locations_file_name {str} -- Locations file name
        rest_file_name {str} -- Results file name
    '''

    uniq_locations = list(rest_file_name)
    results = load_rest(rest_file_name)
    i = results[-1][0] + 1
    while i < len(uniq_locations):
        try:
            g = geocoder.arcgis(uniq_locations[i])
            print(f'{i}:{len(uniq_locations)}:{uniq_locations[i]} - {g.latlng}')
            results.append((i, uniq_locations[i], g.latlng))
            i += 1
        except KeyboardInterrupt:
            break
    pickle.dump(results, open(locations_file_name, 'wb'))


def convert_to_dict(coordinates_file_name, dict_file):
    '''Function coneverts coordinates data to dictionary and saves it to file
    
    Arguments:
        coordinates_file_name {str} -- coordinates file name
        dict_file {dict} -- Name of file to save result dictionary
    '''

    locations = pickle.load(open(coordinates_file_name, 'rb'))
    result_dict = {}
    for var in locations:
        result_dict[var[1]] = var[-1]
    pickle.dump(result_dict, open(dict_file, 'wb'))


def main():
    locations = input('Locations file: ')
    rest = input('Rest file: ')
    coordinates = input('Coordinates file: ')
    dictionary = input('Dictionary file: ')
    geocode(locations, rest)
    convert_to_dict(coordinates, dictionary)


if __name__ == '__main__':
    main()
