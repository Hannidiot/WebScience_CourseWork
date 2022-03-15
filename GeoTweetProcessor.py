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
                lat, lon = self.calc_postition(tweet)
                self.geo_cnt += 1
                if lat > -1 and lon > -1:
                    tweet['lat_index'] = lat
                    tweet['lon_index'] = lon
                    self.num_tweets_by_grid[lat][lon] += 1
            except:
                pass
        
        self.tweets.append(tweet)

    def calc_postition(self, tweet):
        longtitude, latitude = tweet['coordinates']['coordinates']

        for i in range(len(self.rowPoints)):
            if latitude < self.rowPoints[i]:
                # row_index = len(self.rowPoints) - i - 1
                lat_index = i - 1
                break
        
        for i in range(len(self.columnPoints)):
            if longtitude < self.columnPoints[i]:
                # column_index = len(self.columnPoints) - i - 1
                lon_index = i - 1
                break

        return lat_index, lon_index


def plot_heatmap(grids):
    sns.heatmap(grids, vmax=50, vmin=0)


def plot_histmap(grids):
    grid_units = []
    for rows in grids:
        grid_units.extend([item for item in rows if item != 0])

    print(max(grid_units))
    plt.figure(figsize=(10, 5.5) ,dpi=140)
    plt.hist(grid_units, bins = 1400)
    plt.gca().set(xlim=(0, 1400), ylabel='Number of Documents', xlabel='Document Word Count')
    plt.tick_params(size=16)
    plt.xticks(np.linspace(0,1400,8))

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

    # plot_heatmap(processor.num_tweets_by_grid)
    plot_histmap(processor.num_tweets_by_grid)
    plt.show()
