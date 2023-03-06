import sys

def main():

    k, input_file_name = getArgs()

    data = getDataFromFile(input_file_name)

    clusters = [[0,0] for i in range(k)]

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

if __name__ == '__main__':
    main()
