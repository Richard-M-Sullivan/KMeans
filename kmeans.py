import sys
import math

class ClusterData:
    def __init__(self,k,data):
        #set k, points in data with random cluster assignment
        self.k = k

        self.data = {
            'points':[point for point in data],
            'cluster':[i%k for i in range(len(data))]}
        
        # then get the initial cluster centers from the random
        # cluster assignment
        self.old_clusters = None
        self.clusters = [ [0,0] for i in range(self.k)]
        self.calculateClusters()

    def calculateClusters(self):
        self.old_clusters = self.clusters

        sum_of_points_in_cluster = [[0,0] for i in range(k)]
        number_of_points_in_cluster = [0 for i in range(k)]

        # first we sum up the points in a cluster and keep track of how
        # many points are in the cluster
        for i in range(len(self.data['points'])):
            number_of_points_in_cluster[self.data['cluster'][i]] += 1

            sum_of_points_in_cluster[self.data['cluster'][i]] = list(
                map(lambda x: x[0]+x[1],
                    zip(sum_of_points_in_cluster[self.data['cluster'][i]],self.data['points'][i])))
        
        # then we divide the sum of points in a cluster by the number of points
        # in the cluster. or if the sum of points is 0, then we return the original
        # cluster center
        for i in range(len(self.clusters)):
            if number_of_points_in_cluster[i] == 0:
                sum_of_points_in_cluster[i] = self.clusters[i]
            else:
                sum_of_points_in_cluster[i] = list(
                    map(lambda x: x/number_of_points_in_cluster[i],
                        sum_of_points_in_cluster[i]))
        
        self.clusters = sum_of_points_in_cluster

    def claculateClusterAssignment(self):

        for i in range(len(self.data['points'])):
            self.data['cluster'][i] = getClosestPoint(self.data['points'][i],self.clusters)

    def getDistance(point_1,point_2):
        return math.sqrt(sum(map(lambda x: (x[0]-x[1]) ** 2, zip(point_1,point_2))))

    def getClosestCluster(self,point):

        distances = list(map(lambda cluster: getDistance(point,cluster), self.clusters))
        return distances.index(distances.min())

        #neighbor_index = 0
        #for i, point in enumerate(neighboring_points):
        #    dist = getDistance(starting_point,point)
        #    if dist < minDist:
        #        neighbor_index = i
        #        minDist = dist
        #
        #return neighbor_index

    def getDelta(self):
        return max(map(lambda i: getDistance(self.old_clusters[i],self.clusters[i]),
                       range(len(self.clusters))))
    
    def printClusters(self):
        print('Clusters')

        for cluster in self.clusters:
            print(cluster)
        
        print()

    def printData(self):
        print('Point\t\tCluster')

        for i in range(len(self.data['points'])):
            print(self.data['points'][i],self.data['cluster'][i])

        print()



def main():

    k, input_file_name = getArgs()
    data = getDataFromFile(input_file_name)

    data = assignToCluster(data,k)
    
    cluster_centers = [[0,0,0] for i in range(k)]
    new_cluster_centers = calculateClusters(data,k,cluster_centers)

    while(max(map(lambda centers: getDistance(centers[0],centers[1]),
                  zip(cluster_centers, new_cluster_centers))) > 10):

        cluster_centers = new_cluster_centers

        data = assignToCluster(data, k, cluster_centers)

        new_cluster_centers = calculateClusters(data,k,cluster_centers)

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
            #data_entry.append(0)

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

def calculateClusters(data,k,old_cluster_centers):
    cluster_centers = [[0,0] for i in range(k)]
    points_in_cluster = [0 for i in range(k)]

    for point in data:
        points_in_cluster[point[2]] += 1
        cluster_centers[point[2]] = list(map(lambda x: x[0]+x[1], zip(cluster_centers[point[2]],point[:2])))
    
    for i, cluster in enumerate(cluster_centers):
        if points_in_cluster[i] == 0:
            cluster_centers[i] = old_cluster_centers[i]
        else:
            cluster_centers[i] = list(map(lambda x: (x, x/points_in_cluster[i])[points_in_cluster[i] != 0], cluster))
    
    return cluster_centers

def printData(data):
    for point in data:
        print(point)
    print()

if __name__ == '__main__':
    #main()

    k, input_file_name = getArgs()
    k=2
    data = getDataFromFile(input_file_name)

    cluster_data = ClusterData(k,data)

    cluster_data.printClusters()
    cluster_data.printData()
    print('delta',cluster_data.getDelta())

    while(cluster_data.getDelta() > 1):

        cluster_data.claculateClusterAssignment()
        cluster_data.calculateClusters()
        cluster_data.printClusters()
        cluster_data.printData()
        print('delta',cluster_data.getDelta())

    