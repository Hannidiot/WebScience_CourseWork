import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from GeoGrid import GeoGrid


class GeoTweetProcessor:
    def __init__(self, boundary_coordiantes):
        self.boundary_coordiantes = boundary_coordiantes
        self.tweets = []

        # Create Geo Grid Map
        self.geo_grid = GeoGrid(self.boundary_coordiantes)
        self.geo_grid.createGrid()
        self.rowPoints = self.geo_grid.rowPoints
        self.columnPoints = self.geo_grid.colPoints
        self.num_tweets_by_grid = np.zeros((self.geo_grid.rows, self.geo_grid.columns))
        self.geo_cnt = 0

    def add_tweet(self, tweet):

        if tweet.get('geoenabled', False) == True:
            try:
                row, column = self.calc_postition(tweet)
                self.geo_cnt += 1
                if row > -1 and column > -1:
                    tweet['row_index'] = row
                    tweet['column_index'] = column
                    self.num_tweets_by_grid[row][column] += 1
            except:
                pass
        
        self.tweets.append(tweet)

    def calc_postition(self, tweet):
        left_bottom = tweet['place_coordinates'][0][0]
        longtitude, latitude = left_bottom

        for i in range(len(self.rowPoints)):
            if latitude < self.rowPoints[i]:
                # row_index = len(self.rowPoints) - i - 1
                row_index = i - 1
                break
        
        for i in range(len(self.columnPoints)):
            if longtitude < self.columnPoints[i]:
                # column_index = len(self.columnPoints) - i - 1
                column_index = i - 1
                break

        return row_index, column_index


def plot_heatmap(grids):
    sns.heatmap(grids, vmin=0, vmax=50)
    plt.show()


if __name__ == '__main__':
    import json

    samples = []
    with open('data/geoLondonJan', 'r') as f:
        for line in f.readlines():
            samples.append(json.loads(line))
    
    London = [
        -0.563, 51.261318,
        0.28036, 51.686031
    ]

    processor = GeoTweetProcessor(London)
    for sample in samples:
        processor.add_tweet(sample)

    plot_heatmap(processor.num_tweets_by_grid)