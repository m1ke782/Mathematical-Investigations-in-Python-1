#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define min(a,b) ((a>b)?b:a)

int randint(int a, int b)
{
    return (rand()%(b-a+1))+a;
}

void shuffle(int *array, int n)
{
    for (int i = n-1; i >= 0; i--)
    {
        int j = randint(0,i);
        int tmp = array[i];
        array[i] = array[j];
        array[j] = tmp;
    }
}

int* generate_input()
{
    int* cars = (int*)malloc(sizeof(int)*500);
    for (int i = 0; i < 30; i++)
        cars[i] = randint(600,2000);
    for (int i = 0; i < 70; i++)
        cars[30+i] = randint(500,599);
    for (int i = 0; i < 100; i++)
        cars[100+i] = randint(450,499);
    for (int i = 0; i < 200; i++)
        cars[200+i] = randint(400,449);
    for (int i = 0; i < 100; i++)
        cars[400+i] = randint(350,399);
    shuffle(cars, 500);
    return cars;
}

void print_arr(float* arr, int n)
{
    printf("[");
    for (int i = 0; i < n; i++)
    {
        printf("%f",arr[i]);
        if (i+1 != n)
            printf(",");
    }
    printf("]\n");
}

int get_first_lane(int car_len, int* lane_sums, int lanes, int capacity)
{
    for (int i = 0; i < lanes; i++)
    {
        if (lane_sums[i] + car_len <= capacity)
            return i;
    }
    return -1;
}

int get_emptiest_lane(int car_len, int* lane_sums, int lanes, int capacity)
{
    int emptiest_lane = -1;
    int emptiest_lane_size = capacity+1;

    for (int i = 0; i < lanes; i++)
    {
        if (lane_sums[i] + car_len <= capacity && lane_sums[i] < emptiest_lane_size)
        {
            emptiest_lane = i;
            emptiest_lane_size = lane_sums[i];
        }
    }

    return emptiest_lane;
}

int get_fullest_lane(int car_len, int* lane_sums, int lanes, int capacity)
{
    int fullest_lane = -1;
    int fullest_lane_size = -1;

    for (int i = 0; i < lanes; i++)
    {
        if (lane_sums[i] + car_len <= capacity && lane_sums[i] > fullest_lane_size)
        {
            fullest_lane = i;
            fullest_lane_size = lane_sums[i];
        }
    }

    return fullest_lane;
}

int get_random_lane(int car_len, int* lane_sums, int lanes, int capacity)
{
    int* suitable_lanes = (int*)calloc(lanes, sizeof(int));
    int no_suitable_lanes = 0;

    for (int i = 0; i < lanes; i++)
    {
        if (lane_sums[i] + car_len <= capacity)
        {
            suitable_lanes[no_suitable_lanes] = i;
            no_suitable_lanes++;
        }
    }

    int l = -1;
    if (no_suitable_lanes != 0)
        l = suitable_lanes[randint(0,no_suitable_lanes-1)];
    free(suitable_lanes);
    return l;
}

int get_overflow(int* cars, int no_cars, int lanes, int capacity, int (*selector)(int, int*, int, int))
{
    int* lane_sums = (int*)calloc(lanes, sizeof(int));
    int overflow = 0;

    for (int i = 0; i < no_cars; i++)
    {
        int lane_to_place = selector(cars[i], lane_sums, lanes, capacity);
        if (lane_to_place == -1)
            overflow+=cars[i];
        else
            lane_sums[lane_to_place] += cars[i];
    }

    free(lane_sums);
    return overflow;
}

int comp(const void* a, const void* b)
{
    int A = *((int*)a);
    int B = *((int*)b);

    if (A == B) return 0;
    if (A > B) return -1;
    return 1;
}

int get_overflow_sorting_k(int* cars, int no_cars, int lanes, int capacity, int k, int (*selector)(int, int*, int, int))
{
    int* lane_sums = (int*)calloc(lanes, sizeof(int));
    int overflow = 0;

    for (int j = 0; j < no_cars; j+=k)
    {
        qsort(cars+j, min(k,no_cars-j), sizeof(int), comp);
    
        for (int i = j; i < min(no_cars,j+k); i++)
        {
            int lane_to_place = selector(cars[i], lane_sums, lanes, capacity);
            if (lane_to_place == -1)
                overflow+=cars[i];
            else
                lane_sums[lane_to_place] += cars[i];
        }
    }

    free(lane_sums);
    return overflow;
}

int main(void)
{
    srand(time(NULL));

    /*
    int trials = 10000;

    float* s1 = (float*)calloc(500, sizeof(float));
    float* s2 = (float*)calloc(500, sizeof(float));
    float* s3 = (float*)calloc(500, sizeof(float));
    float* s4 = (float*)calloc(500, sizeof(float));

    for (int k = 1; k <= 500; k++)
    {
        printf("%d...\n",k);
        float a1 = 0;
        float a2 = 0;
        float a3 = 0;
        float a4 = 0;
        for (int i = 0; i < trials; i++)
        {
            int* cars = generate_input();
            a1 += (float)get_overflow_sorting_k(cars, 500, 85, 3000, k, get_first_lane);
            a2 += (float)get_overflow_sorting_k(cars, 500, 85, 3000, k, get_emptiest_lane);
            a3 += (float)get_overflow_sorting_k(cars, 500, 85, 3000, k, get_fullest_lane);
            a4 += (float)get_overflow_sorting_k(cars, 500, 85, 3000, k, get_random_lane);
            free(cars);
        }
        s1[k-1]=a1/trials;
        s2[k-1]=a2/trials;
        s3[k-1]=a3/trials;
        s4[k-1]=a4/trials;
    }

    print_arr(s1, 500);
    print_arr(s2, 500);
    print_arr(s3, 500);
    print_arr(s4, 500);
    */


    
    /*
    //int cars[500] = {363, 558, 355, 497, 1845, 406, 421, 466, 369, 443, 359, 421, 440, 1724, 596, 429, 590, 428, 391, 590, 440, 576, 438, 572, 394, 531, 385, 356, 410, 482, 576, 350, 487, 461, 500, 589, 423, 508, 416, 495, 564, 446, 407, 432, 432, 425, 403, 541, 437, 528, 430, 539, 378, 437, 381, 433, 437, 541, 444, 448, 408, 432, 370, 436, 493, 406, 427, 434, 557, 476, 407, 410, 389, 433, 553, 576, 454, 547, 438, 560, 470, 487, 422, 475, 366, 479, 435, 422, 536, 399, 876, 430, 454, 400, 440, 368, 377, 479, 375, 422, 413, 356, 403, 400, 450, 513, 400, 410, 549, 406, 1865, 895, 428, 408, 433, 558, 431, 588, 416, 480, 596, 351, 579, 1098, 445, 444, 1327, 551, 430, 402, 441, 477, 585, 437, 429, 486, 403, 390, 450, 433, 1610, 415, 1259, 531, 410, 416, 449, 443, 362, 402, 382, 487, 433, 436, 407, 466, 515, 416, 467, 565, 388, 644, 479, 450, 360, 432, 415, 497, 357, 389, 481, 474, 492, 1560, 423, 381, 494, 450, 484, 439, 394, 543, 386, 540, 490, 430, 465, 403, 394, 431, 378, 423, 439, 485, 424, 498, 360, 598, 569, 411, 423, 385, 485, 423, 549, 424, 378, 371, 444, 375, 366, 407, 401, 423, 469, 358, 437, 485, 382, 1524, 430, 460, 490, 414, 415, 364, 376, 432, 372, 1397, 417, 413, 437, 412, 1260, 387, 375, 449, 356, 457, 479, 430, 498, 480, 370, 353, 407, 428, 461, 406, 380, 445, 472, 411, 464, 352, 395, 581, 430, 600, 402, 401, 1920, 418, 501, 478, 375, 449, 1750, 470, 431, 541, 414, 437, 414, 372, 386, 404, 377, 447, 435, 423, 435, 598, 401, 560, 455, 553, 391, 446, 458, 485, 406, 438, 1879, 471, 599, 432, 440, 412, 404, 448, 353, 705, 423, 478, 432, 549, 362, 595, 445, 440, 432, 402, 465, 411, 453, 519, 376, 406, 447, 483, 440, 409, 422, 479, 591, 391, 406, 448, 367, 1160, 448, 462, 1225, 450, 436, 366, 425, 465, 367, 435, 526, 552, 469, 415, 379, 368, 566, 437, 429, 379, 387, 585, 563, 456, 1629, 368, 459, 461, 359, 427, 474, 1406, 463, 596, 413, 522, 417, 409, 363, 547, 514, 482, 769, 486, 414, 454, 398, 441, 454, 515, 510, 402, 570, 482, 718, 398, 373, 478, 410, 435, 377, 402, 413, 354, 420, 468, 431, 364, 361, 438, 545, 419, 497, 485, 369, 417, 412, 472, 490, 497, 361, 534, 377, 351, 377, 436, 417, 585, 410, 439, 466, 406, 394, 478, 375, 383, 1344, 531, 390, 474, 401, 385, 497, 1816, 458, 500, 442, 458, 415, 476, 477, 493, 1294, 480, 449, 435, 449, 432, 474, 489, 559, 388, 581, 1744, 440, 372, 375, 427, 388, 368, 1258, 421, 489, 416, 551, 422, 452, 400, 416, 409, 1157, 391, 362, 395, 490, 449, 560, 416, 377, 437, 481, 491, 434, 434, 493, 410, 492, 434, 451, 448, 463, 416, 594, 398, 444, 419, 366, 447};
    int trials = 10000;
    int avg = 0;
    for (int i = 0; i < trials; i++)
    {
        int* cars = generate_input();
        avg += get_overflow(cars, 500, 85, 3000, get_first_lane);
        free(cars);
    }
    printf("%f\n",((float)(avg))/((float)(trials)));

    */

    int trials = 1000;
    int n_max = 729;
    float* s1 = (float*)calloc(n_max, sizeof(int));
    float* s2 = (float*)calloc(n_max, sizeof(int));
    float* s3 = (float*)calloc(n_max, sizeof(int));
    float* s4 = (float*)calloc(n_max, sizeof(int));
    for (int n = 1; n <= n_max; n++)
    {
        printf("%d\n",n);
        int a1 = 0;
        int a2 = 0;
        int a3 = 0;
        int a4 = 0;
        for (int i = 0; i < trials; i++)
        {
            int* cars = generate_input();   
            a1 += get_overflow(cars, 500, n, 255000/n, get_first_lane);
            a2 += get_overflow(cars, 500, n, 255000/n, get_emptiest_lane);
            a3 += get_overflow(cars, 500, n, 255000/n, get_fullest_lane);
            a4 += get_overflow(cars, 500, n, 255000/n, get_random_lane);
            free(cars);
        }
        s1[n-1] = ((float)(a1)) / ((float)(trials));
        s2[n-1] = ((float)(a2)) / ((float)(trials));
        s3[n-1] = ((float)(a3)) / ((float)(trials));
        s4[n-1] = ((float)(a4)) / ((float)(trials));
    }

    print_arr(s1, n_max);
    print_arr(s2, n_max);
    print_arr(s3, n_max);
    print_arr(s4, n_max);
    free(s1);
    free(s2);
    free(s3);
    free(s4);
    

    return 0;
}