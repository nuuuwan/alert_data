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
    def _build_node_query(node_filter: str) -> str:
        """Build a common query template for node queries."""
        return f"""
        [out:json][timeout:{Overpass.TIMEOUT}];
        area["name"="{Overpass.COUNTRY}"]["boundary"="administrative"]["admin_level"="2"]->.country;
        (
        node[{node_filter}](area.country);
        );
        out center;
        """

    @staticmethod
    def download_cities():
        query = Overpass._build_node_query('"place"~"city|town|village"')
        Overpass._fetch_and_save(query, "_overpass_cities")

    @staticmethod
    def download_hospitals():
        query = Overpass._build_node_query('"amenity"="hospital"')
        Overpass._fetch_and_save(query, "_overpass_hospitals")

    @staticmethod
    def download_police_stations():
        query = Overpass._build_node_query('"amenity"="police"')
        Overpass._fetch_and_save(query, "_overpass_police_stations")

    @staticmethod
    def download_fire_stations():
        query = Overpass._build_node_query('"amenity"="fire_station"')
        Overpass._fetch_and_save(query, "_overpass_fire_stations")

    @staticmethod
    def download_all():
        Overpass.download_cities()
        Overpass.download_hospitals()
        Overpass.download_police_stations()
        Overpass.download_fire_stations()
