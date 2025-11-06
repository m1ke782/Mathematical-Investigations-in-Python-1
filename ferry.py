import random

def printSol(S, overflow):
    # Print a solution S and overflow
    for i in range(len(S)):
        print("Ln", i, "\t", sum(S[i]), "cm\t", S[i])
    print("Overflow = " + str(overflow))
    print("Total length in overflow = ", sum(overflow), "cm")


def getFirstLane(carLen, S, c):
    # Return the index of the first suitable lane for the current car.
    # Return -1 is there is no suitable lane
    for i in range(len(S)):
        if sum(S[i]) + carLen <= c:
            return i
    return -1


def getEmptiestLane(carLen, S, c) : 
    # Return the index of the emptiest suitable lane for the current car.
    # Return -1 is there is no suitable lane
    emptiestLane = -1
    emptiestLaneSize = c + 1
    for i in range(len(S)) : 
        if sum(S[i]) < emptiestLaneSize and (sum(S[i]) + carLen <= c) : 
            emptiestLaneSize = sum(S[i])
            emptiestLane = i
    return emptiestLane

def getFullestLane(carLen, S, c) : 
    # Return the index of the fullest suitable lane for the current car.
    # Return -1 is there is no suitable lane
    fullestLane = -1
    fullestLaneSize = -1
    for i in range(len(S)) : 
        if sum(S[i]) > fullestLaneSize and (sum(S[i]) + carLen <= c) : 
            fullestLaneSize = sum(S[i])
            fullestLane = i
    return fullestLane

def getRandomLane(carLen, S, c) : 
    # Return the index of a random suitable lane for the current car.
    # Return -1 is there is no suitable lane
    suitableLanes = []
    for i in range(len(S)) : 
        if sum(S[i]) + carLen <= c : 
            suitableLanes.append(i)

    if len(suitableLanes) == 0 : 
        return -1
    
    return random.choice(suitableLanes)

def generateRandomInput() : 
    cars = []
    for i in range(100) : 
        cars.append(random.randint(350,399))
    for i in range(200) : 
        cars.append(random.randint(400,449))
    for i in range(100) : 
        cars.append(random.randint(450,499))
    for i in range(70) : 
        cars.append(random.randint(500,599))
    for i in range(30) : 
        cars.append(random.randint(600,2000))

    random.shuffle(cars)
    return cars

def getOverflow(numLanes, c, L, laneSelector) : 
    S = [[] for i in range(numLanes)]
    overflow = []
    for i in range(len(L)):
        carLen = L[i]
        lane = laneSelector(carLen, S, c)
        if lane != -1:
            S[lane].append(carLen)
        else:
            overflow.append(carLen)

    return overflow

def main():
    # Read the problem file. All car lengths are put into the list L
    L = []
    with open("input.txt", "r") as f:
        c = int(f.readline())
        numLanes = int(f.readline())
        for line in f:
            L.append(int(line))

    # Output some basic information
    print("Number of vehicles           = " + str(len(L)))
    print("Total length of vehicles     = " + str(sum(L)) + " cm")
    print("Number of lanes              = " + str(numLanes))
    print("Capacity per lane            = " + str(c) + " cm")
    print("List of all vehicle lengths  = " + str(L))

    # Declare the remaining data structures
    S = [[] for i in range(numLanes)]
    overflow = []

    # Here is the basic algorithm.
    for i in range(len(L)):
        carLen = L[i]
        lane = getFullestLane(carLen, S, c)
        if lane != -1:
            S[lane].append(carLen)
        else:
            overflow.append(carLen)

    # Print details of the solution to the screen
    printSol(S, overflow)


if __name__ == "__main__":
    main()
    #print(generateRandomInput())