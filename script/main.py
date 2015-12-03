#
# Sort gifts by
# Try to take as many gifts as possible for each trip.
#

import pandas as pd

import santa

MAX_LOAD = santa.WEIGHT_LIMIT - santa.SLEIGH_WEIGHT


def load_data():
    return pd.read_csv('../data/gifts.csv')


def find_trips(df):
    df = df.sort(['Longitude'])
    trip_id = 0
    weight = 0
    for i, row in df.iterrows():
        weight += row.Weight
        if weight > MAX_LOAD:
            trip_id += 1
            weight = row.Weight
        df.set_value(i, 'TripId', trip_id)
        dist = santa.haversine((row.Latitude, row.Longitude), santa.NORTH_POLE)
        df.set_value(i, 'dist', dist)
    return df.sort(['TripId', 'dist'])


def save_solution(df):
    df[['GiftId', 'TripId']].to_csv('../data/solution.csv', index=False)


def solution():
    print('Load data...')
    data = load_data()
    print('Find trips...')
    trips = find_trips(data)
    print('Save trips...')
    save_solution(trips)
    print('Calculate score for %d trips...' % len(trips))
    score = santa.weighted_reindeer_weariness(trips)
    print(score)


solution()
