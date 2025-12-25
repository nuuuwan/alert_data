from alert import Overpass, Place

if __name__ == "__main__":
    Overpass.download_all()
    Place.build_all()
