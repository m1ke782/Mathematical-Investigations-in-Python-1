import random
import statistics
import matplotlib.pyplot as plt
import scipy

def get_first_lane(car_len, lane_sums, capactity):
    """
    Returns the index of the first lane that still has enough space to hold a new car.

    Inputs : 
        - car_len | int     : the length of the new car to add
        - lane_sums | int[]   : the list of lanes sums, where each element is a the sum of the length of cars in that lane
        - capacity | int    : the maximum capacity of each lane

    Returns : 
        int     : the index of the first lane that can fit a new car. Returns -1 in the case no such lane exists.
    """
    for i in range(len(lane_sums)):
        if lane_sums[i] + car_len <= capactity:
            return i
    return -1

def get_emptiest_lane(car_len, lane_sums, capacity) : 
    """
    Returns the index of the emptiest lane that still has enough space to hold a new car.

    Inputs : 
        - car_len | int     : the length of the new car to add
        - lane_sums | int[]   : the list of lanes sums, where each element is a the sum of the length of cars in that lane
        - capacity | int    : the maximum capacity of each lane

    Returns : 
        int     : the index of the emptiest lane that can fit a new car. Returns -1 in the case no such lane exists.
    """
    emptiest_lane = -1
    emptiest_lane_size = capacity + 1
    for i in range(len(lane_sums)) : 
        if lane_sums[i] < emptiest_lane_size and lane_sums[i] + car_len <= capacity : 
            emptiest_lane_size = lane_sums[i]
            emptiest_lane = i
    return emptiest_lane
    

def get_fullest_lane(car_len, lane_sums, capacity) : 
    """
    Returns the index of the fullest lane that still has enough space to hold a new car.

    Inputs : 
        - car_len | int     : the length of the new car to add
        - lane_sums | int[]   : the list of lanes sums, where each element is a the sum of the length of cars in that lane
        - capacity | int    : the maximum capacity of each lane

    Returns : 
        int     : the index of the fullest lane that can fit a new car. Returns -1 in the case no such lane exists.
    """
    fullest_lane = -1
    fullest_lane_size = -1
    for i in range(len(lane_sums)) : 
        if lane_sums[i] > fullest_lane_size and lane_sums[i] + car_len <= capacity : 
            fullest_lane_size = lane_sums[i]
            fullest_lane = i
    return fullest_lane

def get_random_lane(car_len, lane_sums, capacity) : 
    """
    Returns the index of a random lane that still has enough space to hold a new car.

    Inputs : 
        - car_len | int     : the length of the new car to add
        - lane_sums | int[]   : the list of lanes sums, where each element is a the sum of the length of cars in that lane
        - capacity | int    : the maximum capacity of each lane

    Returns : 
        int     : the index of a random lane that can fit a new car. Returns -1 in the case no such lane exists.
    """
    suitable_lanes = []
    for i in range(len(lane_sums)) : 
        if lane_sums[i] + car_len <= capacity : 
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
    lane_sums = [0 for i in range(num_lanes)]
    overflow = 0
    for i in range(len(cars)):
        car_len = cars[i]
        lane = lane_selector(car_len, lane_sums, capacity)
        if lane != -1:
            lane_sums[lane] += car_len
        else:
            overflow += car_len

    return overflow


def task_1() : 
    cars = []
    with open("input.txt", "r") as f:
        capacity = int(f.readline())
        num_lanes = int(f.readline())
        for line in f:
            cars.append(int(line))

    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    lane_selector = int(input("What lane selectors do you wish to use?  0:First, 1:Emptiest, 2:Fullest, 3:Random "))
    trials = int(input("How many trials do you wish to perform? "))

    avg_overflow_size = sum(get_overflow(num_lanes, capacity, cars, lane_selectors[lane_selector]) for i in range(trials)) / trials
    print("The overflow is : ", avg_overflow_size)

def generate_random_input(shuffled=True) : 
    """
        Generates a random input for the ferry packing problem.

        Inputs : 
            shuffled | bool (optional)  : whether the input is to be shuffled
        
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
    trials = 10000

    samples = []
    for lane_selector in lane_selectors : 
        overflows = [get_overflow(85, 3000, generate_random_input(), lane_selector) for i in range(trials)]
        print("Algorithm ", lane_selector.__name__, " : mean = ", statistics.mean(overflows), "var = ", statistics.variance(overflows))
        samples.append(overflows)

    print(scipy.stats.f_oneway(*samples))
    print(scipy.stats.ttest_ind(samples[0], samples[2], equal_var=False))
    plt.bar_label(plt.bar([l.__name__ for l in lane_selectors], [statistics.mean(sample) for sample in samples]))
    plt.show()


def task_3_a() : 
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 10000

    samples = []
    for lane_selector in lane_selectors : 
        overflows = [get_overflow(85, 3000, generate_random_input(False), lane_selector) for i in range(trials)]
        print("Algorithm ", lane_selector.__name__, " : mean = ", statistics.mean(overflows), "var = ", statistics.variance(overflows))
        samples.append(overflows)

    print(scipy.stats.f_oneway(*samples))
    print(scipy.stats.ttest_ind(samples[0], samples[2], equal_var=False))
    plt.bar_label(plt.bar([l.__name__ for l in lane_selectors], [statistics.mean(sample) for sample in samples]))
    plt.show()

def get_overflow_sorting_k(num_lanes, capacity, cars, lane_selector, k) : 
    """
    Returns the the total length of cars in the overflow carpark.

    Inputs : 
        - num_lanes | int       : the number of lanes
        - capacity | int        : the maximum capacity of each lane
        - cars| int[]           : the list of car lengths
        - lane_selector | func  : the lane sector function, takes in (car_len, lanes, capacity) as parameters are returns the lane index 
        - k | int               : the number of cars to consider in one chunk

    Returns : 
        int     : the total length of cars in the overflow carpark.
    """
    lane_sums = [0 for i in range(num_lanes)]
    overflow = 0
    for i in range(0, len(cars), k):
        next_k_cars = [cars[i+j] for j in range(0,k) if i+j < len(cars)]
        next_k_cars.sort(reverse=True)

        for j in range(len(next_k_cars)) : 
            car_len = next_k_cars[j]
            lane = lane_selector(car_len, lane_sums, capacity)
            if lane != -1:
                lane_sums[lane] += car_len
            else:
                overflow += car_len

    return overflow

def task_3_b() : 
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 10000

    for lane_selector in lane_selectors : 
        overflow_against_k = []
        for k in range(1,501) : 
            overflows = sum([get_overflow_sorting_k(85, 3000, generate_random_input(), lane_selector, k) for i in range(trials)]) / trials
            overflow_against_k.append(overflows)
        print(scipy.stats.spearmanr(range(1,501), overflow_against_k))
        plt.plot(overflow_against_k)
    plt.show()

def task_3_c() : 
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 1000

    for lane_selector in lane_selectors : 
        overflow_against_lane_number = []
        for no_lanes in range(1,730) : 
            overflows = sum([get_overflow(no_lanes, 3000*85/no_lanes, generate_random_input(), lane_selector) for i in range(trials)]) / trials
            overflow_against_lane_number.append(overflows)
        print(scipy.stats.spearmanr(range(1,730), overflow_against_lane_number))
        plt.plot(overflow_against_lane_number)
    plt.show()


def greedy_lane_overflow(no_lanes, capacity, cars) : 
    cars_left = cars.copy()
    cars_left.sort(reverse=True)

    for i in range(no_lanes) : 
        lane_sum = 0
        j = 0
        while j < len(cars_left) : 
            if lane_sum + cars_left[j] <= capacity : 
                lane_sum += cars_left[j]
                del cars_left[j]
            else : 
                j += 1
    return sum(cars_left)

def task_3_d() : 
    trials = 10000
    overflows = [greedy_lane_overflow(85, 3000, generate_random_input()) for i in range(trials)]
    print(statistics.mean(overflows))

task_3_d()