import random
import statistics
import matplotlib.pyplot as plt
import scipy

def get_first_lane(car_len, lanes, capactity):
    """
    Returns the index of the first lane that still has enough space to hold a new car.

    Inputs : 
        - car_len | int     : the length of the new car to add
        - lanes | int[][]   : the list of lanes, where each lane is a list of car lengths
        - capacity | int    : the maximum capacity of each lane

    Returns : 
        int     : the index of the first lane that can fit a new car. Returns -1 in the case no such lane exists.
    """
    for i in range(len(lanes)):
        if sum(lanes[i]) + car_len <= capactity:
            return i
    return -1

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
            emptiest_lane_size = sum(lanes[i])
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

    return sum(overflow)


def task_1() : 
    cars = []
    with open("input.txt", "r") as f:
        capacity = int(f.readline())
        num_lanes = int(f.readline())
        for line in f:
            cars.append(int(line))

    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    lane_selector = int(input("What lane selector do you wish to use? 0:First, 1:Emptiest, 2:Fullest, 3:Random "))
    trials = int(input("How many trials do you wish to perform? "))

    avg_overflow_size = sum(get_overflow(num_lanes, capacity, cars, lane_selectors[lane_selector]) for i in range(trials)) / trials
    print("The overflow is : ", avg_overflow_size)

def generate_random_input(shuffled=True) : 
    """
        Generates a random input for the ferry packing problem.

        Inputs : 
            none
        
        Returns : 
            int[] : list of vehicle lengths
    """
    cars = []
    for i in range(30) : 
        cars.append(random.randint(600,2000))
    for i in range(70) : 
        cars.append(random.randint(500,599))
    for i in range(100) : 
        cars.append(random.randint(450,499))
    for i in range(200) : 
        cars.append(random.randint(400,449))
    for i in range(100) : 
        cars.append(random.randint(350,399))
    
    if shuffled : 
        random.shuffle(cars)
    return cars

def task_2() : 
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 1000

    samples = []
    for lane_selector in lane_selectors : 
        overflows = [get_overflow(85, 3000, generate_random_input(), lane_selector) for i in range(trials)]
        print("Algorithm ", lane_selector, " : ")
        print(" The average overflow is : ", statistics.mean(overflows))
        print(" The variance of overflow is : ", statistics.variance(overflows))
        samples.append(overflows)

    print(scipy.stats.f_oneway(*samples))

def task_3_a() : 
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 1000

    samples = []
    for lane_selector in lane_selectors : 
        overflows = [get_overflow(85, 3000, generate_random_input(False), lane_selector) for i in range(trials)]
        print("Algorithm ", lane_selector, " : ")
        print(" The average overflow is : ", statistics.mean(overflows))
        print(" The variance of overflow is : ", statistics.variance(overflows))
        samples.append(overflows)

    print(scipy.stats.f_oneway(*samples))

task_3_a()