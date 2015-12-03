import pandas as pd

import santa


def load_data():
    return pd.read_csv('../data/gifts.csv')


def distance_from_polar(row):
    return santa.haversine((row['Latitude'], row['Longitude']), santa.NORTH_POLE)


def minimal_cost(df):
    df['distance'] = df.apply(distance_from_polar, axis=1)
    df['cost'] = df['distance'] * df['Weight']
    return df.cost.sum()/(10**9)


def main():
    data = load_data()
    print('Minimal cost: %f' % minimal_cost(data))
    avg_weight = data['Weight'].mean()
    print('Average weight: %f' % avg_weight)
    trip_count = (len(data)*avg_weight)/(santa.WEIGHT_LIMIT-santa.SLEIGH_WEIGHT)
    print('Expected number of trips: %f' % trip_count)


main()
