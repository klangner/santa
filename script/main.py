#
# Sort gifts by
# Try to take as many gifts as possible for each trip.
#

import pandas as pd

import santa


def load_data():
    return pd.read_csv('../data/gifts.csv')


def get_distance(item):
    return item[1]


def find_trips(df):
    df = df.sort(['Longitude'])
    trips = []
    gifts = []
    weight = 0
    for i, row in df.iterrows():
        if weight + row.Weight > santa.WEIGHT_LIMIT - santa.SLEIGH_WEIGHT:
            trips.append(gifts)
            gifts = []
            weight = 0
        weight += row.Weight
        gifts.append((row.GiftId, santa.haversine((row.Latitude, row.Longitude), santa.NORTH_POLE)))
    trips.append(gifts)
    xs = [sorted(trip, key=get_distance) for trip in trips]
    return to_pandas(xs)


def save_solution(df):
    df[['GiftId', 'TripId']].to_csv('../data/solution.csv', index=False)


def to_pandas(trips):
    trip_series = []
    gift_series = []
    with open('../data/solution.csv', "a") as f:
        f.write('GiftId,TripId')
        for trip_id, gifts in enumerate(trips):
            for (gift_id, _) in gifts:
                gift_series.append(int(gift_id))
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
