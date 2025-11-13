import tqdm
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
    trials = 1000

    samples = []
    for lane_selector in lane_selectors : 
        overflows = [get_overflow(85, 3000, generate_random_input(), lane_selector) for i in range(trials)]
        print("Algorithm ", lane_selector, " : ")
        print(" The average overflow is : ", statistics.mean(overflows))
        print(" The variance of overflow is : ", statistics.variance(overflows))
        samples.append(overflows)

    print(scipy.stats.f_oneway(*samples))


def task_2b() : 
    trials = 1000
    X_1 = [get_overflow(85, 3000, generate_random_input(), get_first_lane) for i in range(1000)]
    X_2 = [get_overflow(85, 3000, generate_random_input(), get_fullest_lane) for i in range(1000)]
    print(scipy.stats.ttest_ind(X_1,X_2, equal_var = False))

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
    lanes = [[] for i in range(num_lanes)]
    overflow = []
    for i in range(0, len(cars), k):
        next_k_cars = [cars[i+j] for j in range(0,k) if i+j < len(cars)]
        next_k_cars.sort(reverse=True)

        for j in range(len(next_k_cars)) : 
            car_len = next_k_cars[j]
            lane = lane_selector(car_len, lanes, capacity)
            if lane != -1:
                lanes[lane].append(car_len)
            else:
                overflow.append(car_len)

    return sum(overflow)

def task_3_b() : 
    lane_selectors = [get_first_lane]
    trials = 1000

    for lane_selector in lane_selectors : 
        overflow_against_k = []
        for k in tqdm.tqdm(range(1,251)) : 
            overflows = sum([get_overflow_sorting_k(85, 3000, generate_random_input(), lane_selector, 500) for i in range(trials)]) / trials
            overflow_against_k.append(overflows)
        plt.plot(overflow_against_k)
        print(overflow_against_k)
    plt.show()
#[2783.526, 2892.818, 2865.445, 2822.532, 2825.049, 2824.412, 2802.071, 2839.63, 2886.037, 2888.531, 2810.378, 2822.272, 2797.878, 2860.2, 2838.637, 2819.652, 2852.195, 2898.045, 2891.074, 2839.382, 2832.688, 2850.802, 2913.626, 2852.922, 2826.122, 2777.329, 2890.865, 2807.405, 2965.501, 2727.488, 2775.779, 2841.876, 2906.231, 2859.545, 2995.782, 2798.923, 2918.441, 2887.815, 2824.449, 2884.289, 2882.704, 3008.456, 2960.205, 2897.282, 2878.483, 2893.854, 2961.98, 2858.767, 2836.943, 2817.433, 2916.056, 2876.403, 3092.064, 2870.245, 2870.526, 2925.159, 2839.931, 2876.543, 2835.011, 2787.893, 2881.79, 2946.027, 2733.027, 2961.449, 2802.714, 2946.122, 2938.423, 2934.227, 2881.714, 2820.846, 2878.602, 2924.244, 2776.808, 2832.858, 2974.339, 2818.111, 2743.963, 2918.536, 2952.61, 3047.7, 2861.524, 2799.993, 2875.812, 2830.042, 2808.126, 2799.401, 2898.67, 2856.18, 2844.648, 2937.418, 2982.194, 2983.922, 2782.117, 2878.557, 2798.147, 2926.223, 2946.645, 2942.844, 2964.809, 3006.898, 2813.362, 2862.46, 2923.956, 2743.31, 2872.331, 2946.865, 2972.698, 2812.396, 2769.312, 2751.639, 2840.282, 2873.495, 2772.912, 2862.697, 2831.344, 2855.746, 2898.698, 2784.04, 2962.063, 2876.395, 2898.956, 2830.634, 2866.634, 2894.586, 2794.195, 2855.717, 2905.711, 2842.902, 2787.329, 2892.875, 2825.129, 2973.364, 2851.073, 2848.558, 2812.739, 2888.149, 2845.206, 2907.01, 2829.421, 2886.08, 2874.568, 2849.989, 2880.354, 2819.507, 2924.023, 2800.964, 2864.756, 2925.301, 2903.364, 2962.06, 2826.0, 2923.877, 2810.338, 2785.051, 2865.208, 2878.747, 2932.199, 2900.331, 2793.085, 2881.761, 2838.624, 2879.923, 2857.928, 2948.391, 2907.956, 2936.731, 2940.63, 2929.448, 2890.099, 2944.976, 2923.729, 2810.397, 2784.261, 2823.63, 2759.636, 2921.026, 2848.884, 2808.979, 2842.885, 2929.828, 2829.259, 2863.854, 2753.324, 2764.984, 2853.592, 2842.514, 2950.208, 2958.442, 2880.635, 2940.83, 2817.042, 3041.657, 2854.229, 2913.258, 2818.574, 2840.845, 2811.937, 2872.461, 2850.794, 2900.049, 2816.749, 2884.239, 2828.491, 2985.073, 2956.344, 2872.102, 2886.133, 2819.914, 2879.422, 2876.682, 2863.427, 2839.08, 2870.677, 2873.935, 2838.51, 2859.961, 2937.712, 2923.802, 2824.069, 2894.474, 2934.001, 2892.82, 2793.475, 2910.295, 2956.664, 2832.963, 2856.144, 2894.481, 2830.049, 2807.538, 2807.016, 2879.796, 2743.008, 2803.856, 2814.773, 2868.386, 2782.567, 2893.744, 2823.944, 2875.439, 2832.264, 2878.8, 2843.053, 2776.167, 2885.737, 2982.133, 2906.276, 2864.799, 2866.093, 2889.83]

def task_3_c() : 
    lane_selectors = [get_first_lane, get_emptiest_lane, get_fullest_lane, get_random_lane]
    trials = 500

    for lane_selector in lane_selectors : 
        overflow_against_lane_number = []
        for no_lanes in tqdm.tqdm(range(1,201)) : 
            overflows = sum([get_overflow(no_lanes, 3000*85/no_lanes, generate_random_input(), lane_selector) for i in range(trials)]) / trials
            overflow_against_lane_number.append(overflows)
        plt.plot(overflow_against_lane_number)
        #print(overflow_against_k)
    plt.show()