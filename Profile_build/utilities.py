from datetime import datetime

def read_command(filename):
    # read nfdump command 
    command = list()
    with open(filename, 'r') as file:
        text = file.read().strip()
        command = text.split("\n")
    return command

def datetime_to_timestamp(time_str):
    # convert a datetime string to timestamp
    # example: "2020-08-16 23:04:29.056" 
    # 
    # dtime = datetime(2020, 8, 16, 23, 4, int(29.056))

    dtime = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')

    timestamp = dtime.timestamp()
    print(timestamp)

if __name__ == "__main__":
    # for test
    # print(read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single_defined.txt"))

    datetime_to_timestamp("2020-08-16 23:04:29.056")