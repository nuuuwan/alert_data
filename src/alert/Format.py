class Format:

    @staticmethod
    def lat_lng(lat_lng, precision=4):
        return [round(x, precision) for x in lat_lng]
