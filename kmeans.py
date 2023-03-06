import sys

def main():
    argument_count = len(sys.argv)

    if argument_count < 3:
        print('too few arguments expected a number and a file path')
        return

    if argument_count > 3:
        print('too many arguments expected a number and a file path')
        return

      
    k = 0

    try:
        k = int(sys.argv[1])
    except ValueError:
        print('first parameter was not a number')
        return

    input_file_name = str(sys.argv[2])

    print(k)
    print(input_file_name)



if __name__ == '__main__':
    main()