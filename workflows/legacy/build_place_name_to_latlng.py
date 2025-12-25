from alert import Format, StaticData


def main():
    places = StaticData("_places").read()
    place_name_to_latlng = {
        place["name"]: (Format.lat_lng(place["lat_lng"])) for place in places
    }
    place_name_to_latlng = {
        k: v
        for k, v in sorted(
            place_name_to_latlng.items(), key=lambda item: item[0]
        )
    }
    StaticData("place_name_to_latlng").write(place_name_to_latlng)


if __name__ == "__main__":
    main()
