from utils import Log

from alert import StaticData

log = Log("build_cities")


if __name__ == "__main__":
    _cities_from_overpass = StaticData("_cities_from_overpass").read()

    cities = []
    for elem in _cities_from_overpass["elements"]:

        try:
            tags = elem["tags"]
            population = int(tags.get("population") or 0)
            city = dict(
                name=tags.get("name") or tags.get("name:en"),
                lat_lng=(round(elem["lat"], 4), round(elem["lon"], 4)),
            )
            if not city["name"]:
                log.error(f"Missing name for city with id: {elem['id']}")
                continue

            cities.append(city)
        except KeyError as e:
            log.error(f"Missing expected tag {e} in element {elem['id']}")
            continue

    cities.sort(key=lambda city: city["name"])
    StaticData("cities").write(cities)
