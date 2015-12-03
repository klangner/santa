#
# Sort gifts by
# Try to take as many gifts as possible for each trip.
#

import pandas as pd

import santa


def load_data():
    return pd.read_csv('../data/gifts.csv')


def find_trips(df):
    df['taken'] = False
    trips = []
    for i, row in df.iterrows():
        if not row.taken:
            # gifts, df = add_gifts(df, santa.NORTH_POLE, santa.WEIGHT_LIMIT-santa.SLEIGH_WEIGHT)
            trips.append([1])#gifts)
    return to_pandas(trips)


def add_gifts(df, start_pos, available_weight):
    gifts = []
    min_distance = 10**9
    index = -1
    for i, row in df.iterrows():
        if not row.taken and row.Weight < available_weight:
            pos = row['Latitude'], row['Longitude']
            dist = santa.haversine(start_pos, pos)
            if dist < min_distance:
                index = i
                min_distance = dist
    if index >= 0:
        gifts.append(df.loc[[index]])
        df.set_value(index, 'taken', True)
    return gifts, df


def save_solution(df):
    df[['GiftId', 'TripId']].to_csv('../data/solution.csv', index=False)


def to_pandas(trips):
    trip_series = []
    gift_series = []
    with open('../data/solution.csv', "a") as f:
        f.write('GiftId,TripId')
        for trip_id, gifts in enumerate(trips):
            for gift_id in gifts:
                gift_series.append(gift_id)
                trip_series.append(trip_id)
    return pd.DataFrame({'GiftId': gift_series, 'TripId': trip_series})


def solution():
    print('Load data...')
    data = load_data()
    print('Find trips...')
    trips = find_trips(data)
    print('Save trips...')
    save_solution(trips)
    xs = pd.merge(trips, data, on='GiftId', how='left')
    print('Calculate score for %d trips...' % len(xs))
    score = santa.weighted_reindeer_weariness(xs)
    print(score)


solution()
