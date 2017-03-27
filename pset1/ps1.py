###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    journey = []
    trip = []
    cows_copy = cows.copy()

    def make_trip(cows_copy, limit, trip_weight, current_trip):
        while len(cows_copy.values())!=0 and trip_weight + min(cows_copy.values()) <= limit:
            max_value = limit - trip_weight
            while max_value not in cows_copy.values():
                max_value -= 1
            # biggest = max(cows_copy.values())
            for cow in cows_copy:
                if cows_copy[cow] == max_value:
                    trip_weight += cows_copy.pop(cow)
                    current_trip.append(cow)
                    break
        return current_trip

    while len(cows_copy) != 0:
        trip = make_trip(cows_copy, limit, 0, [])
        journey.append(trip)

    return journey



# Problem 2
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    enumeration = []
    enumeration_dict = {}

    for partition in get_partitions(cows):
        enumeration.append(partition)
    print('done with enumeration', len(enumeration))
    for journey in enumeration:
        trips = []
        if enumeration.index(journey)%10000 == 0:
            print(enumeration.index(journey))
        for trip in journey:
            trip_weight = 0
            for cow in trip:
                trip_weight += cows[cow]
            trips.append(trip_weight)
        enumeration_dict[enumeration.index(journey)] = trips #create new dict of 'journey no.':'trip weight(s)'
    print('done with enum.dict')
    badkeys = [] #identify journeys with trip weights over the limit
    for key,values in enumeration_dict.items():
        for value in values:
            if value > limit:
                badkeys.append(key)
                break
    goodkeys = list(set(enumeration_dict.keys()) - set(badkeys)) #only care about journeys with trip weights under limit.
    print('got good keys')
    if len(goodkeys) > 1: #if more then one, check them against each other
        bestkey = goodkeys[0]
        for key in goodkeys:
            if len(enumeration_dict[key]) < len(enumeration_dict[bestkey]):
                bestkey = key
        return enumeration[bestkey] #return the first journey with the lowest number of trips
    else:
        return enumeration[goodkeys[0]] #otherwise return the only journey




        
# Problem 3
def compare_cow_transport_algorithms(func):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    import datetime

    print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    print('1',func)
    print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
print(cows)

#print(greedy_cow_transport(cows, limit))
compare_cow_transport_algorithms(greedy_cow_transport(cows, limit))
#print(brute_force_cow_transport(cows, limit))
compare_cow_transport_algorithms(brute_force_cow_transport(cows, limit))


