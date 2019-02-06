from LocationsMap.entities import Film, Episode
import re


def create_file_generator(file_path: str):
    with open(file_path, 'r') as file:
        for row in file:
            yield row


def select_year(base: list, year: int):
    base = list(filter(lambda x: x.count('(' + str(year)) == 1, base))
    return base


def read_database(file_name: str):
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


def strip_title(title: str):
    title = title.replace('#', '')
    title = title.replace('"', '')
    title = title.strip()
    return title


def transform(base: list):
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


