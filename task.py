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
    # loop over every lane
    for i in range(len(lane_sums)):
        # return the first one that can fit this vehicle
        if lane_sums[i] + car_len <= capactity:
            return i
        
    # no suitable lane found, return -1
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
    # keep track of the current emptiest lane (currently unknown)
    emptiest_lane = -1
    emptiest_lane_size = capacity + 1

    # loop over each lane
    for i in range(len(lane_sums)) : 
        # if this lane fits this vehicle and is emptier than the current emptiest, replace it
        if lane_sums[i] < emptiest_lane_size and lane_sums[i] + car_len <= capacity : 
            emptiest_lane_size = lane_sums[i]
            emptiest_lane = i

    # return the emptiest suitable lane (if exists)
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
    # keep track of the current fullest lane (currently unknown)
    fullest_lane = -1
    fullest_lane_size = -1

    # loop over every lane
    for i in range(len(lane_sums)) : 
        # if this lane fits this vehicle and is fuller than the current emptiest, replace it
        if lane_sums[i] > fullest_lane_size and lane_sums[i] + car_len <= capacity : 
            fullest_lane_size = lane_sums[i]
            fullest_lane = i

    # return the fullest suitable lane (if exists)
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
    # find all the suitable lanes
    suitable_lanes = []
    for i in range(len(lane_sums)) : 
        if lane_sums[i] + car_len <= capacity : 
            suitable_lanes.append(i)

    # if there is no suitable lane, return -1
    if len(suitable_lanes) == 0 : 
        return -1
    
    # otherwise, return a random suitable lane
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
    # initialise empty lanes and overflow
    lane_sums = [0 for i in range(num_lanes)]
    overflow = 0

    # loop over each car
    for i in range(len(cars)):
        # use the lane selector to find the lane to load this car in
        lane = lane_selector(cars[i], lane_sums, capacity)

        # if a lane was found, add it to the lane
        if lane != -1:
            lane_sums[lane] += cars[i]
        # if no lane was found, add it to the overflow
        else:
            overflow += cars[i]

    # return the total length of cars in the overflow
    return overflow


def task_1() : 
    # read the input file
    cars = []
    with open("input.txt", "r") as f:
        capacity = int(f.readline())
        num_lanes = int(f.readline())
        for line in f:
            cars.append(int(line))
    # these are the lane selectors we wish to test
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]

    # ask the user which lane selector they wish to test, and with how many trials
    lane_selector = int(input("What lane selectors do you wish to use?  0:First, 1:Emptiest, 2:Fullest, 3:Random "))
    trials = int(input("How many trials do you wish to perform? "))

    # perform the test and return the overflow
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
    # add cars of lengths specified by the task
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

    # shuffle the cars if the user asked for it to be shuffled
    if shuffled : 
        random.shuffle(cars)

    # return these cars
    return cars

def task_2() : 
    # we wish to test these lane selectors at this number of trials
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 10000

    # collect the random samples
    samples = []
    for lane_selector in lane_selectors : 
        overflows = [get_overflow(85, 3000, generate_random_input(), lane_selector) for i in range(trials)]
        print("Algorithm ", lane_selector.__name__, " : mean = ", statistics.mean(overflows), "var = ", statistics.variance(overflows))
        samples.append(overflows)

    # perform suitable statistical tests
    print(scipy.stats.f_oneway(*samples))
    print(scipy.stats.ttest_ind(samples[0], samples[2], equal_var=False))

    # produce a pretty picture
    plt.bar_label(plt.bar([l.__name__ for l in lane_selectors], [statistics.mean(sample) for sample in samples]))
    plt.show()


def task_3_a() : 
    # we wish to test these lane selectors at this number of trials
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 10000

    # collect the random samples
    samples = []
    for lane_selector in lane_selectors : 
        overflows = [get_overflow(85, 3000, generate_random_input(False), lane_selector) for i in range(trials)]
        print("Algorithm ", lane_selector.__name__, " : mean = ", statistics.mean(overflows), "var = ", statistics.variance(overflows))
        samples.append(overflows)

    # perform suitable statistical tests
    print(scipy.stats.f_oneway(*samples))
    print(scipy.stats.ttest_ind(samples[0], samples[2], equal_var=False))

    # produce a pretty picture
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
    # initialise empty lanes and overflow
    lane_sums = [0 for i in range(num_lanes)]
    overflow = 0

    # loop over every group of k vehicles
    for i in range(0, len(cars), k):
        # collect the next k vehicles and sort them in descending order
        next_k_cars = [cars[i+j] for j in range(0,k) if i+j < len(cars)]
        next_k_cars.sort(reverse=True)

        # loop over every car in this group of k vehicles
        for j in range(len(next_k_cars)) : 
            # use the provided lane selector to find which lane to place this car
            lane = lane_selector(next_k_cars[j], lane_sums, capacity)

            # if a suitable lane was found, place it there
            if lane != -1:
                lane_sums[lane] += next_k_cars[j]
            # otherwise, add it to the overflow
            else:
                overflow += next_k_cars[j]

    # return the total length of cars in the overflow
    return overflow

def task_3_b() : 
    # we wish to test these lane selectors at this number of trials
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 10000

    # for each lane selector...
    for lane_selector in lane_selectors : 
        # find the overflow as a function of k
        overflow_against_k = []
        for k in range(1,501) : 
            overflows = sum([get_overflow_sorting_k(85, 3000, generate_random_input(), lane_selector, k) for i in range(trials)]) / trials
            overflow_against_k.append(overflows)

        # perform a spearmans rank test for corelation between the overflow and k
        print(scipy.stats.spearmanr(range(1,501), overflow_against_k))

        # add this line to the plot
        plt.plot(overflow_against_k)

    # show the plot
    plt.show()

def task_3_c() : 
    # we wish to test these lane selectors at this number of trials
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 1000

    # for each lane selector...
    for lane_selector in lane_selectors : 
        # find the overflow as a function of n
        overflow_against_lane_number = []
        for no_lanes in range(1,730) : 
            overflows = sum([get_overflow(no_lanes, 3000*85/no_lanes, generate_random_input(), lane_selector) for i in range(trials)]) / trials
            overflow_against_lane_number.append(overflows)

        # perform a spearmans rank test for corelation between the overflow and n
        print(scipy.stats.spearmanr(range(1,730), overflow_against_lane_number))

        # add this line to the plot
        plt.plot(overflow_against_lane_number)

    # show the plot
    plt.show()


def greedy_lane_overflow(no_lanes, capacity, cars) : 
    """
    Returns the overflow after using the greedy lane algorithm.

    Inputs : 
    - num_lanes | int       : the number of lanes
    - capacity | int        : the maximum capacity of each lane
    - cars| int[]           : the list of car lengths

    Returns : 
        int     : the total length of cars in the overflow carpark.
    """
    # keep track of which cars are left
    cars_left = cars.copy()
    cars_left.sort(reverse=True)

    # for each lane...
    for i in range(no_lanes) : 
        # keep track of the size of this lane, and which car we are considering
        lane_sum = 0
        j = 0

        # for each car left...
        while j < len(cars_left) : 
            # if this car fits, add it to the lane and remove it from the car
            if lane_sum + cars_left[j] <= capacity : 
                lane_sum += cars_left[j]
                del cars_left[j]
            else : 
                j += 1

    # return the sum of the lengths of all the remaining cars
    return sum(cars_left)

def task_3_d() : 
    # test the greedy lane overflow at 10000 trials
    trials = 10000
    overflows = [greedy_lane_overflow(85, 3000, generate_random_input()) for i in range(trials)]
    print(statistics.mean(overflows))