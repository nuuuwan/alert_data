from utils import Log

from alert import StaticData

log = Log("build_river_stations")


if __name__ == "__main__":
    _old_river_stations = StaticData("_old_river_stations").read()
    place_name_latlng = StaticData("place_name_to_latlng").read()

    new_river_stations = []
    for river_station in _old_river_stations:
        name = river_station["id"]
        lat_lng = place_name_latlng.get(name)
        if not lat_lng:
            log.error(f"Missing lat_lng for river station: {name}")
        new_river_station = dict(
            lat_lng=lat_lng,
            name=name,
            river_name=river_station["river_name"],
            alert_level_m=river_station["alert_level_m"],
            minor_flood_level_m=river_station["minor_flood_level_m"],
            major_flood_level_m=river_station["major_flood_level_m"],
        )
        new_river_stations.append(new_river_station)

    new_river_stations.sort(key=lambda river_station: river_station["name"])

    StaticData("river_stations").write(new_river_stations)
