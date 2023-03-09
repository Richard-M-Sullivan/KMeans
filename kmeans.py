import random
import sys
import math

def main():
    # get k and the file from argument list
    k = int(sys.argv[1])
    file_name = str(sys.argv[2])

    # parse the file to create a list of points
    points = []
    with open(file_name,'r') as file:
        for line in file:
            points.append(list(map(int,line.split())))
    
    assignment = None
    centroids = None
    failures = 0
    for i in range(10):
        try:
            assignment,centroids = cluster(points,k)
            break
        except:
            if(failures == 0):
                print('clustering failed... trying again')

            failures += 1

    # if the process failed do not write the file and end the program
    if failures == 10:
        print('unable to cluster')
        sys.exit()

    # otherwise print failures and write cluster assignment to a file
    if failures > 0:
        print('clustering failed',failures,'times')

    with open('output.txt','w') as file:
        for i, point in enumerate(points):
            file.write(f'{point[0]} {point[1]} {assignment[i]+1}\n')

def initializeCentroids(points,k):
    # use k and the shape of the data to initialize random centroids
    x_min = int(min(list(point[0] for point in points)))
    x_max = int(max(list(point[0] for point in points)))

    y_min = int(min(list(point[1] for point in points)))
    y_max = int(max(list(point[1] for point in points)))

    centroids = []
    for _ in range(k):
        centroids.append([random.randint(x_min,x_max),random.randint(y_min,y_max)])
    
    return centroids

def getClosestCentroid(point,centroids):
    dist = [getDistance(point,centroid) for centroid in centroids]
    return dist.index(min(dist))

def createCentroids(points,assignment,k):
    centroids = [[0,0] for _ in range(k)]
    point_count = [0 for _ in range(k)]

    # for each centroid a the values of the points that are assigned to that centroid
    for i, point in enumerate(points):
        centroids[assignment[i]] = list(map(sum, zip(centroids[assignment[i]],point)))
        point_count[assignment[i]] = point_count[assignment[i]] + 1
    
    # then divide the sum of all points in each centroid by the number of points in each centorid
    for i in range(len(centroids)):
        centroids[i] = list(map(lambda x: x/point_count[i], centroids[i]))
    
    return centroids
        
def getAssignment(points,centroids):
    return [getClosestCentroid(point,centroids) for point in points]

def getDistance(point_1,point_2):
    return math.sqrt(sum(map(lambda x: (x[0]-x[1]) ** 2, zip(point_1,point_2))))

def cluster(points,k):
    #initialize centroids to random locations and assign points to centroid
    centroids = initializeCentroids(points,k)
    assignment = getAssignment(points,centroids)
    
    # now loop through updating centroids and assignment until it the
    # system stabalizes or the max iteration limit is met
    max_iterations = 100
    for i in range(max_iterations):
        #update centroids and assignments
        old_centroids = centroids
        centroids = createCentroids(points,assignment,k)
        assignment = getAssignment(points,centroids)

        #if the centroids did not move then break
        if max(list(getDistance(old_centroids[i],centroids[i]) for i in range(k))) == 0:
            break

    return (assignment,centroids)

if __name__ == '__main__':
    main()

