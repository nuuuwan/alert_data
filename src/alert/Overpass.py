import requests
from utils import Log

from alert.StaticData import StaticData

log = Log("Overpass")


class Overpass:

    URL = "https://overpass-api.de/api/interpreter"
    TIMEOUT = 25
    COUNTRY = "Sri Lanka"

    @staticmethod
    def get_cities():
        query = f"""
        [out:json][timeout:{Overpass.TIMEOUT}];
        area["name"="{Overpass.COUNTRY}"]["boundary"="administrative"]["admin_level"="2"]->.country;
        (
        node["place"~"city|town|village"](area.country);
        way["place"~"city|town|village"](area.country);
        relation["place"~"city|town|village"](area.country);
        );
        out center;
        """

        response = requests.post(Overpass.URL, data={"data": query})
        response.raise_for_status()
        data = response.json()

        d_list = []
        for el in data["elements"]:
            d = dict(el)
            d_list.append(d)
        StaticData("_cities_from_overpass").write(d_list)


if __name__ == "__main__":
    Overpass.get_cities()
