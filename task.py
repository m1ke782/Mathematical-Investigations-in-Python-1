import random

def get_emptiest_lane(car_len, lanes, capacity) : 
    """
    Returns the index of the emptiest lane that still has enough space to hold a new car.

    Inputs : 
        - car_len | int     : the length of the new car to add
        - lanes | int[][]   : the list of lanes, where each lane is a list of car lengths
        - capacity | int    : the maximum capacity of each lane

    Returns : 
        int     : the index of the emptiest lane that can fit a new car. Returns -1 in the case no such lane exists.
    """
    emptiest_lane = -1
    emptiest_lane_size = capacity + 1
    for i in range(len(lanes)) : 
        if sum(lanes[i]) < emptiest_lane_size and (sum(lanes[i]) + car_len <= capacity) : 
            emptiest_lane = sum(lanes[i])
            emptiest_lane = i
    return emptiest_lane

def get_fullest_lane(car_len, lanes, capacity) : 
    """
    Returns the index of the fullest lane that still has enough space to hold a new car.

    Inputs : 
        - car_len | int     : the length of the new car to add
        - lanes | int[][]   : the list of lanes, where each lane is a list of car lengths
        - capacity | int    : the maximum capacity of each lane

    Returns : 
        int     : the index of the fullest lane that can fit a new car. Returns -1 in the case no such lane exists.
    """
    fullest_lane = -1
    fullest_lane_size = -1
    for i in range(len(lanes)) : 
        if sum(lanes[i]) > fullest_lane_size and (sum(lanes[i]) + car_len <= capacity) : 
            fullest_lane_size = sum(lanes[i])
            fullest_lane = i
    return fullest_lane

def get_random_lane(car_len, lanes, capacity) : 
    """
    Returns the index of a random lane that still has enough space to hold a new car.

    Inputs : 
        - car_len | int     : the length of the new car to add
        - lanes | int[][]   : the list of lanes, where each lane is a list of car lengths
        - capacity | int    : the maximum capacity of each lane

    Returns : 
        int     : the index of a random lane that can fit a new car. Returns -1 in the case no such lane exists.
    """
    suitable_lanes = []
    for i in range(len(lanes)) : 
        if sum(lanes[i]) + car_len <= capacity : 
            suitable_lanes.append(i)

    if len(suitable_lanes) == 0 : 
        return -1
    
    return random.choice(suitable_lanes)

def get_overflow(num_lanes, capacity, cars, lane_selector) : 
    """
    Returns the the total length of cars in the overflow carpark.

    Inputs : 
        - num_lanes | int       : the number of lanes
        - capacity | int        : the maximum capacity of each lane
        - cars| int[]           : the list of car lengths
        - lane_selector | func  : the lane sector function, takes in (car_len, lanes, capacity) as parameters are returns the lane index 

    Returns : 
        int     : the total length of cars in the overflow carpark.
    """
    lanes = [[] for i in range(num_lanes)]
    overflow = []
    for i in range(len(cars)):
        car_len = cars[i]
        lane = lane_selector(car_len, lanes, capacity)
        if lane != -1:
            lanes[lane].append(car_len)
        else:
            overflow.append(car_len)

    return overflow

