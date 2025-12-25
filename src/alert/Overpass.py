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
    def _fetch_and_save(
        query: str, file_id: str, force: bool = False
    ) -> None:
        static_data = StaticData(file_id)
        if static_data.exists() and not force:
            log.info(
                f"Skipping {file_id} - file already exists (use force=True to override)"
            )
            return
        data = Overpass._query_overpass(query)
        elements = Overpass._extract_elements(data)
        static_data.write(elements)

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
    def download_cities(force: bool = False):
        query = Overpass._build_node_query('"place"~"city|town|village"')
        Overpass._fetch_and_save(query, "_overpass_cities", force=force)

    @staticmethod
    def download_hospitals(force: bool = False):
        query = Overpass._build_node_query('"amenity"="hospital"')
        Overpass._fetch_and_save(query, "_overpass_hospitals", force=force)

    @staticmethod
    def download_police_stations(force: bool = False):
        query = Overpass._build_node_query('"amenity"="police"')
        Overpass._fetch_and_save(
            query, "_overpass_police_stations", force=force
        )

    @staticmethod
    def download_fire_stations(force: bool = False):
        query = Overpass._build_node_query('"amenity"="fire_station"')
        Overpass._fetch_and_save(
            query, "_overpass_fire_stations", force=force
        )

    @staticmethod
    def download_all(force: bool = False):
        Overpass.download_cities(force=force)
        Overpass.download_hospitals(force=force)
        Overpass.download_police_stations(force=force)
        Overpass.download_fire_stations(force=force)
