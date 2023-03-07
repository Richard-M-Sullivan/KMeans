import sys
import math

def main():

    k, input_file_name = getArgs()
    data = getDataFromFile(input_file_name)

    data = assignToCluster(data,k)
    cluster_centers = [[0,0,0] for i in range(k)]
    new_cluster_centers = calculateCenters(data,k)

    while(max(map(lambda old,new: getDistance(old,new),
                  zip(cluster_centers, new_cluster_centers))) > 10):

        data = assignToCluster(data, k, new_cluster_centers)
        
        cluster_centers = new_cluster_centers
        new_cluster_centers = calculateCenters(data,k)



    

    for point in sorted(data):
        print(point)

def getArgs():
    # check if the right number of arguments
    argument_count = len(sys.argv)

    if argument_count < 3:
        print('too few arguments expected a number and a file path')
        sys.exit()
    if argument_count > 3:
        print('too many arguments expected a number and a file path')
        sys.exit()

    # ckeck if k is an int
    k = None
    try:
        k = int(sys.argv[1])
    except ValueError:
        print('first parameter was not a number')
        sys.exit()

    input_file_name = str(sys.argv[2])

    return (k,input_file_name)


def getDataFromFile(input_file_name):
    data = []

    try:
        input_file = open(input_file_name,'r')
    except FileNotFoundError:
        print('The input file was not found')
        sys.exit()
    except:
        print('an file error occured')
        sys.exit()
    else:
        # the cluster is assigned 0 to start
        for i, entry in enumerate(input_file):
            data_entry = list(map(int,entry.split()))
            data_entry.append(0)

            data.append(data_entry)
    finally:
        input_file.close()

    return data

def getDistance(point_1,point_2):
    return math.sqrt(sum(map(lambda x: (x[0]-x[1]) ** 2, zip(point_1,point_2))))

def getClosestPoint(starting_point,neighboring_points):
    minDist = getDistance(starting_point,neighboring_points[0])
    neighbor_index = 0
    for i, point in enumerate(neighboring_points):
        dist = getDistance(starting_point,point)
        if dist < minDist:
            neighbor_index = i
            minDist = dist

    return neighbor_index

def assignToCluster(points,k,cluster_points=None):
    new_points = []

    if cluster_points == None:
        new_points = [[point[0], point[1], i%k] for i, point in enumerate(points)]
    else:
        for point in points:
            new_points.append([point[0], point[1], getClosestPoint(point,cluster_points)])

    return new_points

def calculateClusters(data,k):
    cluster_centers = [[0,0] for i in range(k)]
    points_in_cluster = [0 for i in range(k)]

    for point in data:
        points_in_cluster[point[2]] += 1
        cluster_centers[point[2]] = list(map(lambda x: x[0]+x[1], zip(cluster_centers[point[2]],point[:2])))
    
    for i, cluster in enumerate(cluster_centers):
        cluster_centers[i] = list(map(lambda x: x/points_in_cluster[i], cluster))
    
    return cluster_centers


if __name__ == '__main__':
    #main()
    data = [
        [1,2,0],
        [1,3,1],
        [2,1,2],
        [5,5,0],
        [5,1,1],
        [6,2,2],
        [5,2,0],
        [3,4,1],
        [3.5,5.2,2],
        [4.1,4.2,0]
    ]

    for point in data:
        print(point)
    
    cluster = calculateClusters(data,k=3)
    print('\n',cluster,'\n')

    for i in range(10):
        data = assignToCluster(data,k=3,cluster_points=cluster)
        cluster =calculateClusters(data,k=3)
        for point in data:
            print(point)
        
        print('\n',cluster,'\n')