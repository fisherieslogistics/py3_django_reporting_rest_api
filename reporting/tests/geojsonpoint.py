import random


def maybe(percent=50):
    return random.randrange(100) < percent


def geojsonpoint(config):
    lat = config['lat']
    lon = config['lon']

    def thegenerator():
        latmove = random.randrange(10) / 1000
        lonmove = random.randrange(10) / 1000
        newlat = lat
        newLon = lon
        if(maybe()):
            newlat -= latmove
        else:
            newlat += latmove
        if(maybe()):
            newLon -= lonmove
        else:
            newLon += lonmove
        gp = 'POINT({} {})'.format(newlat, newLon)

        while(True):
            yield gp

    return thegenerator


def geopoint(config):
    return geojsonpoint(config)()


GENERATORS = {'geojsonpoint': geopoint}
