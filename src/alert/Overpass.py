import time

import requests
from utils import Log

from alert.StaticData import StaticData

log = Log("Overpass")


class Overpass:

    URL = "https://overpass-api.de/api/interpreter"
    TIMEOUT = 25
    COUNTRY = "Sri Lanka"

    @staticmethod
    def _query_overpass(query: str) -> dict:
        time.sleep(2)
        response = requests.post(Overpass.URL, data={"data": query})
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _extract_elements(data: dict) -> list:
        return [dict(el) for el in data.get("elements", [])]

    @staticmethod
    def _fetch_and_save(query: str, file_id: str) -> None:
        data = Overpass._query_overpass(query)
        elements = Overpass._extract_elements(data)
        StaticData(file_id).write(elements)

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
        Overpass._fetch_and_save(query, "_overpass_cities")

    @staticmethod
    def get_hospitals():
        query = f"""
        [out:json][timeout:{Overpass.TIMEOUT}];
        area["name"="{Overpass.COUNTRY}"]["boundary"="administrative"]["admin_level"="2"]->.country;
        (
        node["amenity"="hospital"](area.country);
        way["amenity"="hospital"](area.country);
        relation["amenity"="hospital"](area.country);
        );
        out center;
        """
        Overpass._fetch_and_save(query, "_overpass_hospitals")

    @staticmethod
    def get_police_stations():
        query = f"""
        [out:json][timeout:{Overpass.TIMEOUT}];
        area["name"="{Overpass.COUNTRY}"]["boundary"="administrative"]["admin_level"="2"]->.country;
        (
        node["amenity"="police"](area.country);
        way["amenity"="police"](area.country);
        relation["amenity"="police"](area.country);
        );
        out center;
        """
        Overpass._fetch_and_save(query, "_overpass_police_stations")

    @staticmethod
    def get_fire_stations():
        query = f"""
        [out:json][timeout:{Overpass.TIMEOUT}];
        area["name"="{Overpass.COUNTRY}"]["boundary"="administrative"]["admin_level"="2"]->.country;
        (
        node["amenity"="fire_station"](area.country);
        way["amenity"="fire_station"](area.country);
        relation["amenity"="fire_station"](area.country);
        );
        out center;
        """
        Overpass._fetch_and_save(query, "_overpass_fire_stations")
