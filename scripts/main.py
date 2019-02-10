import os
from pathlib import Path
from LocationsMap.map import create_map
import os


def main():
    type_of_request = input(
        'If you want to build map for all films be year type 1, else if you want to build map by country type 2: ')

    while not (type_of_request in ['1', '2']):
        print('Choose number of appropriate range!')
        type_of_request = input(
            'If you want to build map for all films be year type 1, else if you want to build map by country type 2: ')
    type_of_request = int(type_of_request)
    if type_of_request == 1:
        year = input('Type year: ')
        while not all(list(map(lambda x: x.isdigit(), year))):
            print('Year should be number! ')
            year = input('Type year: ')
        year = int(year)
        limit = input('To speed up the execution of the program you can set how much films will be displayed on '
                      'the map, otherwise leave this blank: ')

        while not all(list(map(lambda x: x.isdigit() or x == '', limit))):
            print('Limit should be number or blank line! ')
            limit = input('To speed up the execution of the program you can set how much films will be displayed on '
                          'the map, otherwise leave this blank: ')
        if limit != '':
            limit = int(limit)
    elif type_of_request == 2:
        country = input('Type country: ')
        limit = input(
            'To speed up the execution of the program you can set how much films will be displayed on the map, '
            'otherwise leave this blank: ')
        while not all(list(map(lambda x: x.isdigit() or x == '', limit))):
            print('Limit should be number or blank line! ')
            limit = input('To speed up the execution of the program you can set how much films will be displayed on '
                          'the map, otherwise leave this blank: ')
        if limit != '':
            limit = int(limit)
    second_layer = input('Select type of additional data to display: 1 to display population, 2 to display films heatmap: ')
    while not (second_layer in ['1', '2']):
        print('Choose number of appropriate range!')
        second_layer = input('Select type of additional data to display: 1 to display population, 2 to display films heatmap: ')
    second_layer = int(second_layer)
    result_file = input('Type name of map file:')
    limit = limit if limit !='' else None
    if type_of_request == 1:
        create_map(type_of_request, year, result_file, second_layer, limit)
    elif type_of_request == 2:
        create_map(type_of_request, country, result_file, second_layer, limit)


if __name__ == '__main__':
    print(Path(os.getcwd()).parent)
    main()
