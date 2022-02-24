import json
import math

samples = []
with open('data/geoLondonJan', 'r') as f:
    for line in f.readlines():
        samples.append(json.loads(line))

london_left_top = [-0.563, 51.261318]

def computeDistance(location1, location2):
    R = 6371.0
    lat1, lon1 = location1
    lat2, lon2 = location2

    phi1 = lat1 * (math.pi / 180)
    phi2 = lat2 * (math.pi / 180)
    delta1 = (lat2 - lat1) * (math.pi / 180)
    delta2 = (lon2 - lon1) * (math.pi / 180)

    a = math.sin(delta1 / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta2 / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c

    return d

for sample in samples:
    locations = sample['place_coordinates'][0]
    distance = computeDistance(london_left_top, locations[0])
    print(distance)
