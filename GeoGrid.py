import numpy as np
import math


class GeoGrid:
    def __init__(self, bounding):
        self.boundingCoordinates = bounding

    def computeDistance(self, long2, lat2):
        R = 6373.0
        lat1 = self.boundingCoordinates[1]
        long1 = self.boundingCoordinates[0]

        phi1 = lat1 * (math.pi / 180)
        phi2 = lat2 * (math.pi / 180)
        delta1 = (lat2 - lat1) * (math.pi / 180)
        delta2 = (long2 - long1) * (math.pi / 180)

        a = math.sin(delta1 / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta2 / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c

        return d

    def createGrid(self):
        self.rows = int(np.ceil(self.computeDistance(self.boundingCoordinates[0], self.boundingCoordinates[3])))
        print(f'number of rows is: {self.rows}')

        self.columns = int(np.ceil(self.computeDistance(self.boundingCoordinates[2], self.boundingCoordinates[1])))
        print(f'number of columns is: {self.columns}')

        self.noofGrids = int(self.rows * self.columns)
        print(f'number of grids is: {self.noofGrids}')

        self.colMax = int(np.ceil(self.computeDistance(self.boundingCoordinates[2], self.boundingCoordinates[1])))
        print(f'number of maximum columns is: {self.colMax}')

        self.rowPoints = []
        self.colPoints = []
        self.lonOffset = (self.boundingCoordinates[2] - self.boundingCoordinates[0]) / self.columns
        self.latOffset = (self.boundingCoordinates[3] - self.boundingCoordinates[1]) / self.rows

        for i in range(self.rows):
            self.rowPoints.append(self.boundingCoordinates[1] + i * self.latOffset)
        for j in range(self.columns):
            self.colPoints.append(self.boundingCoordinates[0] + j * self.lonOffset)


if __name__ == "__main__":
    London = [
        -0.563, 51.261318,
        0.28036, 51.686031
    ]

    NewYork = [-74.255653,40.495682,-73.689484,40.917622]
    geo = GeoGrid(NewYork)
    geo.createGrid()
