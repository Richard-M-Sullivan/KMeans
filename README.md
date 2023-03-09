# KMeans
Simple k-means implementation for a university assignment

## Summary
The program takes in the number of clusters to create and the path to the
data file that you want to cluster. Then the program labels the data into
clusters and saves the information in a file called output.txt

## Usage
To use the program call 'python3 kmeans.py' followed by two arguments:

* a number: Sets the value of k (the number of clusters)
* a string: The path to the input data file

Example: python3 kmeans.py 3 ./input_file.txt

Note that the input file needs to be a text file, and the format of the file
should be two numbers per line separated by a space.

Example Input File:
10 11
5 3
213 5
15 23

### Output
The output is in the format of three numbers per line separated by spaces.
The first two numbers are the point from the input file, and the third number
is the cluster that the point was assigned to. the data is saved to a file
called output.txt

Example Output File:
10 11 0
5 3 1
213 5 3
15 23