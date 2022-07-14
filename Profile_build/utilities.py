from datetime import datetime
from datetime import timezone
from datetime import timedelta

def read_command(filename):
    # read nfdump command 
    command = list()
    with open(filename, 'r') as file:
        text = file.read().strip()
        command = text.split("\n")
    return command

def datetime_to_timestamp(time_str):
    # convert a datetime string to timestamp
    # example: "2020-08-16 23:04:29.056" => 1597644269.056
    # 
    # dtime = datetime(2020, 8, 16, 23, 4, int(29.056))

    # add the time zone information
    # I am reading this from Eugene during the summer, so the time zone is -0700
    # please change this accordingly, otherwise the program cannot be correct
    time_str = time_str + ":-0700"

    dtime = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f:%z')

    timestamp = dtime.timestamp()
    # print(timestamp)
    return timestamp

def timestamp_to_datetime(ts):
    # convert a timestamp to datetime string and further convert it to the time format we need
    # example: 1597644269.056 => "2020-08-16 23:04:29.056"
    # 00:04

    # the Netflow is from FRGP, whose timezone is -6 
    # please change this accordingly, otherwise the program cannot be correct
    timezone_offset = timedelta(hours = -6)
    datetime_obj = datetime.fromtimestamp(ts, tz=timezone(timezone_offset))

    return str(datetime_obj.strftime("%H:%M"))

if __name__ == "__main__":
    # for test
    # print(read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single_defined.txt"))

    datetime_to_timestamp("2020-08-16 23:04:29.056")