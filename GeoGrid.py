import numpy as np


class GeoGrid:
    def __init__(self, bounding):
        self.boundingCoordinates = bounding

    def computeDistance(self, lat2, long2):
        R = 6371.0
        lat1 = self.boundingCoordinates[1]
        long1 = self.boundingCoordinates[0]
        # lat2 = self.boundingCoordinates[3]
        # long2 = self.boundingCoordinates[2]

        phi1 = lat1 * (np.pi / 180)
        phi2 = lat2 * (np.pi / 180)
        delta1 = (lat2 - lat1) * (np.pi / 180)
        delta2 = (long2 - long1) * (np.pi / 180)

        a = np.sin(delta1 / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta2 / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        d = R * c

        return d


if __name__ == "__main__":
    London = [
        -0.563, 51.261318, 
        0.28036, 51.686031
    ]

    geo = GeoGrid(London)
    print(geo.computeDistance(*[
                    -0.1114755,
                    51.4194247
                ]))
