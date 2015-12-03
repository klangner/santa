#
# Sort gifts by
# Try to take as many gifts as possible for each trip.
#

import pandas as pd
import santa


def load_data():
    return pd.read_csv('../data/gifts.csv')


def greedy(df):
    """
    Try to get all gifts every time
    :param df: data
    :return: DataFrame with trip id
    """
    # Sort dataframe by longitude
    df = df.sort(['Longitude', 'Latitude'])
    df['TripId'] = 0
    trip_id = 0
    weight = 0
    for i, row in df.iterrows():
        weight += row['Weight']
        if weight > (santa.WEIGHT_LIMIT - santa.SLEIGH_WEIGHT)/2:
            trip_id += 1
            weight = santa.SLEIGH_WEIGHT + row['Weight']
        df.set_value(i, 'TripId', trip_id)
    return df


def greedy2(df):
    """
    Try to get 2 gifts every time
    :param df: data
    :return: DataFrame with trip id
    """
    df = df.sort(['Longitude', 'Latitude'])
    trip_id = -1
    df['TripId'] = 0
    last_pos = santa.NORTH_POLE
    for i, row in df.iterrows():
        pos = row['Longitude'], row['Latitude']
        if i % 2 == 0 or santa.haversine(pos, last_pos) > santa.haversine(pos, santa.NORTH_POLE)/3:
            trip_id += 1
            last_pos = pos
        df.set_value(i, 'TripId', trip_id)
    return df


def save_solution(df):
    df[['GiftId', 'TripId']].to_csv('../data/solution.csv', index=False)


data = load_data()
solution = greedy2(data)
save_solution(solution)
score = santa.weighted_reindeer_weariness(solution)
print(score)
