#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define min(a,b) ((a>b)?b:a)

int randint(int a, int b)
{
    static int seed = 0;
    seed++;
    srand(time(0)+seed);
    return (rand()%(b-a+1))+a;
}

void shuffle(int *array, size_t n)
{
    if (n > 1) 
    {
        size_t i;
        for (i = 0; i < n - 1; i++) 
        {
          size_t j = i + rand() / (RAND_MAX / (n - i) + 1);
          int t = array[j];
          array[j] = array[i];
          array[i] = t;
        }
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

int get_overflow(int* cars, int no_cars, int lanes, int capacity)
{
    int* lane_sums = (int*)calloc(lanes, sizeof(int));
    int overflow = 0;

    for (int i = 0; i < no_cars; i++)
    {
        int lane_to_place = get_random_lane(cars[i], lane_sums, lanes, capacity);
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

    /*
    int trials = 10000;
    float avg = 0;
    for (int i = 0; i < trials; i++)
    {
        int* cars = generate_input();
        avg += (float)get_overflow(cars, 500, 85, 3000);
        free(cars);
    }
    printf("%f\n",avg/(float)(trials));
    */

    return 0;
}