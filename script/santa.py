from math import radians, cos, sin, asin, sqrt

AVG_EARTH_RADIUS = 6371  # in km

NORTH_POLE = (90, 0)
SLEIGH_WEIGHT = 10
WEIGHT_LIMIT = 1000


def haversine(point1, point2):
    """ Calculate the great-circle distance bewteen two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance between the two points.
    """
    # unpack latitude/longitude
    lat1, lng1 = point1
    lat2, lng2 = point2

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(lng / 2) ** 2
    return 2 * AVG_EARTH_RADIUS * asin(sqrt(d))


def weighted_trip_length(stops, weights):
    tuples = [tuple(x) for x in stops.values]
    # adding the last trip back to north pole, with just the sleigh weight
    tuples.append(NORTH_POLE)
    weights.append(SLEIGH_WEIGHT)

    dist = 0.0
    prev_stop = NORTH_POLE
    prev_weight = sum(weights)
    for i in range(len(tuples)):
        dist += haversine(tuples[i], prev_stop) * prev_weight
        prev_stop = tuples[i]
        prev_weight = prev_weight - weights[i]
    return dist


def weighted_reindeer_weariness(all_trips):
    uniq_trips = all_trips.TripId.unique()

    if any(all_trips.groupby('TripId').Weight.sum() + SLEIGH_WEIGHT > WEIGHT_LIMIT):
        raise Exception("One of the sleighs over weight limit!")

    dist = 0
    for t in uniq_trips:
        this_trip = all_trips[all_trips.TripId == t]
        dist = dist + weighted_trip_length(this_trip[['Latitude', 'Longitude']], this_trip.Weight.tolist())

    return dist/(10**9)
