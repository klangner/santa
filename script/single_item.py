#
# Just take single item
#

import pandas as pd
import santa


def load_data():
    return pd.read_csv('../data/gifts.csv')


def single(df):
    """
    Best result: 29 * 10^9
    :param df:
    :return:
    """
    df['TripId'] = 0
    for i, row in df.iterrows():
        df.set_value(i, 'TripId', i)
    return df


def save_solution(df):
    df[['GiftId', 'TripId']].to_csv('../data/solution.csv', index=False)


data = load_data()
solution = single(data)
save_solution(solution)
score = santa.weighted_reindeer_weariness(solution)
print(score)

