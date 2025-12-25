from alert.StaticData import StaticData


class Place:
    @staticmethod
    def build_cities():
        places_from_overpass = StaticData("_overpass_cities").read()

        cities = []
        for elem in places_from_overpass:

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

                if population < 10_000:
                    continue

                cities.append(city)
            except KeyError as e:
                log.error(f"Missing expected tag {e} in element {elem['id']}")
                continue

        cities.sort(key=lambda city: city["name"])
        StaticData("cities").write(cities)
