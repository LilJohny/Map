import geocoder


def set_coordinates(base: list):
    for i in range(len(base)):
        base[i].coordinates = geocoder.yandex(base[i].location)
    return base
