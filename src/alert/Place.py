from utils import Log

from alert.StaticData import StaticData

log = Log("Place")


class Place:
    @staticmethod
    def _build_places(
        input_key: str,
        output_key: str,
        entity_type: str,
        min_population: int = 0,
    ) -> None:
        places_from_overpass = StaticData(input_key).read()

        places = []
        for overpass_place in places_from_overpass:

            try:
                tags = overpass_place["tags"]
                place = dict(
                    name=tags.get("name") or tags.get("name:en"),
                    lat_lng=(
                        round(overpass_place["lat"], 4),
                        round(overpass_place["lon"], 4),
                    ),
                )
                if not place["name"]:
                    log.error(
                        f"Missing name for {entity_type} with id: {
                            overpass_place['id']}"
                    )
                    continue

                if min_population > 0:
                    population = int(tags.get("population") or 0)
                    if population < min_population:
                        continue

                places.append(place)
            except KeyError as e:
                log.error(
                    f"Missing expected tag {e} in element {
                        overpass_place['id']}"
                )
                continue

        places.sort(key=lambda p: p["name"])
        StaticData(output_key).write(places)

    @staticmethod
    def build_cities():
        Place._build_places(
            "_overpass_cities", "cities", "city", min_population=10_000
        )

    @staticmethod
    def build_hospitals():
        Place._build_places("_overpass_hospitals", "hospitals", "hospital")

    @staticmethod
    def build_police_stations():
        Place._build_places(
            "_overpass_police_stations", "police_stations", "police station"
        )

    @staticmethod
    def build_fire_stations():
        Place._build_places(
            "_overpass_fire_stations", "fire_stations", "fire station"
        )

    @staticmethod
    def build_all():
        Place.build_cities()
        Place.build_hospitals()
        Place.build_police_stations()
        Place.build_fire_stations()
