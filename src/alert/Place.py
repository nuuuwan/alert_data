from utils import Log

from alert.StaticData import StaticData

log = Log("Place")


class Place:
    @staticmethod
    def build_cities():
        places_from_overpass = StaticData("_overpass_cities").read()

        places = []
        for overpass_place in places_from_overpass:

            try:
                tags = overpass_place["tags"]
                population = int(tags.get("population") or 0)
                place = dict(
                    name=tags.get("name") or tags.get("name:en"),
                    lat_lng=(
                        round(overpass_place["lat"], 4),
                        round(overpass_place["lon"], 4),
                    ),
                )
                if not place["name"]:
                    log.error(
                        f"Missing name for city with id: {overpass_place['id']}"
                    )
                    continue

                if population < 10_000:
                    continue

                places.append(place)
            except KeyError as e:
                log.error(
                    f"Missing expected tag {e} in element {overpass_place['id']}"
                )
                continue

        places.sort(key=lambda city: city["name"])
        StaticData("cities").write(places)
