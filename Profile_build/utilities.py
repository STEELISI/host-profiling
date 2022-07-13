from datetime import datetime

def read_command(filename):
    # read nfdump command 
    command = list()
    with open(filename, 'r') as file:
        text = file.read().strip()
        command = text.split("\n")
    return command

def datetime_to_timestamp():
    dtime = datetime(2020, 8, 16, 23, 4, int(29.056))
    timestamp = dtime.timestamp()
    print(timestamp)

if __name__ == "__main__":
    # for test
    # print(read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single_defined.txt"))

    datetime_to_timestamp()