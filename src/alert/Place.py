from utils import Log

from alert.StaticData import StaticData

log = Log("Place")


class Place:
    @staticmethod
    def _extract_lat_lng(overpass_place: dict) -> tuple:
        """Extract lat/lng from either top level or center object."""
        if "lat" in overpass_place and "lon" in overpass_place:
            lat = overpass_place["lat"]
            lon = overpass_place["lon"]
        elif "center" in overpass_place:
            lat = overpass_place["center"]["lat"]
            lon = overpass_place["center"]["lon"]
        else:
            raise KeyError("lat/lng not found in place or center")
        return (round(lat, 4), round(lon, 4))

    @staticmethod
    def dedupe_by_name(places: list) -> None:
        seen = set()
        duplicates = []
        for place in places:
            if place["name"] in seen:
                duplicates.append(place)
            else:
                seen.add(place["name"])
        for place in duplicates:
            places.remove(place)

    @staticmethod
    def dedupe_by_latlng(places: list) -> None:
        PRECISION = 2
        seen = set()
        duplicates = []
        for place in places:
            lat, lng = place["lat_lng"]
            crude_latlng = (round(lat, PRECISION), round(lng, PRECISION))
            if crude_latlng in seen:
                duplicates.append(place)
            else:
                seen.add(crude_latlng)
        for place in duplicates:
            places.remove(place)

    @staticmethod
    def dedupe(places: list) -> None:
        Place.dedupe_by_name(places)
        Place.dedupe_by_latlng(places)

    @staticmethod
    def _build_places(
        input_key: str,
        output_key: str,
        entity_type: str,
        min_population: int = 0,
        name_placeholder: str = None,
    ) -> None:
        places_from_overpass = StaticData(input_key).read()

        places = []
        for overpass_place in places_from_overpass:

            try:
                tags = overpass_place["tags"]
                place = dict(
                    name=tags.get("name") or tags.get("name:en"),
                    lat_lng=Place._extract_lat_lng(overpass_place),
                )
                if not place["name"]:
                    log.warning(
                        f"Missing name for {entity_type} with id: {
                            overpass_place['id']}"
                    )
                    if name_placeholder:
                        place["name"] = name_placeholder
                    else:
                        continue

                place["name"] = " ".join(
                    [
                        word[0].upper() + word[1:]
                        for word in place["name"].strip().split()
                    ]
                )

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
        Place.dedupe(places)
        StaticData(output_key).write(places)

    @staticmethod
    def build_cities():
        Place._build_places(
            input_key="_overpass_cities",
            output_key="cities",
            entity_type="city",
            min_population=10_000,
        )

    @staticmethod
    def build_hospitals():
        Place._build_places(
            input_key="_overpass_hospitals",
            output_key="hospitals",
            entity_type="hospital",
            name_placeholder="Hospital",
        )

    @staticmethod
    def build_police_stations():
        Place._build_places(
            input_key="_overpass_police_stations",
            output_key="police_stations",
            entity_type="police station",
        )

    @staticmethod
    def build_fire_stations():
        Place._build_places(
            input_key="_overpass_fire_stations",
            output_key="fire_stations",
            entity_type="fire station",
            name_placeholder="Fire Station",
        )

    @staticmethod
    def build_all():
        Place.build_cities()
        Place.build_hospitals()
        Place.build_police_stations()
        Place.build_fire_stations()
