# from calendar import day_abbr
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import os
import json
import time

def get_folders(folder):
    # get all the folders on the first layer of a path
    subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
    return subfolders

def get_files(path):
    # path = '/data/2019'
    files = []
    ## r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if 'nfcapd.' in file:
                files.append(os.path.join(r, file))
    # for f in files:
    #     print(f)

    return files

def get_all_files(path):
    # path = '/data/2019'
    files = []
    ## r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    # for f in files:
    #     print(f)

    return files

def read_list_from_file_linebyline(filename):
    res_list = []
    with open(filename, 'r') as file:
        text = file.read().strip()
        res_list = text.split("\n")
    return res_list

def save_port_usage_to_file(port_usage_list, filename):
    # save the port usage information to a file 
    # line by line 

    print("Start saving ......")
    saving_start_time = time.time()
    
    # read the file name 
    dirname = os.path.dirname(__file__)
    absolute_filename = os.path.join(dirname, filename)

    with open(absolute_filename, 'w') as port_usage_file:
        num = 1
        for item in port_usage_list:
            port_usage_file.write(item[0] + "," + str(num) + "," + str(item[1][0]) + "," + str(item[1][1]) + "\n")
            num += 1

    saving_end_time = time.time()
    saving_time_taken = saving_end_time - saving_start_time
    print("Saving completed and toke " + str(saving_time_taken) + " s.")

def save_list_to_file_linebyline(list, filename):
    # read the file name 
    dirname = os.path.dirname(__file__)
    absolute_filename = os.path.join(dirname, filename)

    with open(absolute_filename, 'w') as list_file:
        for i in list:
            list_file.write(i+'\n')

def read_command(filename):
    # read nfdump command 
    command = list()
    with open(filename, 'r') as file:
        text = file.read().strip()
        command = text.split("\n")
    return command

def service_port_to_dict(filename):
    # read the port information and return a dictionary

    print("Reading service ports ...")
    ports_dict = dict()
    ports_info = list()
    with open(filename, 'r') as file:
        text = file.read().strip()
        ports_info = text.split("\n")

    count = 0
    for line in ports_info:
        count += 1
        if count == 1:
            continue
        count += 1
        items = line.split(",")
        if len(items) < 10:
            continue
        if "Unassigned" in items[3]:
            continue
        if "Reserved" in items[3]:
            continue
        # print(line)
        ports_dict[items[1]]=items[0]
    print("Service ports loaded sucessfully!")
    return ports_dict


def dict_write_to_file(dict,filename):
    # write the dictionary to a txt file
    # input the dictionary first, then the filename
    
    print("Saving results to " + filename + " ......")
    start_time = time.time()

    with open(filename, 'w') as convert_file:
        convert_file.write(json.dumps(dict))

    end_time = time.time()
    print("Results saved!")
    print("Toke " + str(end_time-start_time) + " s.")

def dict_read_from_file(filename):
    # Read data from a file and convert it to a dictionary

    print("Reading data from " + filename + " ......")
    start_time = time.time()

    with open(filename) as json_file:
        data_dict = json.load(json_file)
    
    end_time = time.time()
    print("Data read successfully!")
    print("Toke " + str(end_time-start_time) + " s.")

    return data_dict

def merge_dict(dict1, dict2):
    # merge two dictionaries 
    result = {**dict1, **dict2}
    return result

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
    # => 00:04

    # the Netflow is from FRGP, whose timezone is -6 
    # please change this accordingly, otherwise the program cannot be correct
    timezone_offset = timedelta(hours = -6)
    datetime_obj = datetime.fromtimestamp(ts, tz=timezone(timezone_offset))

    # return datetime_obj
    return str(datetime_obj.strftime("%H:%M"))

def time_round_day(ts):
    # the Netflow is from FRGP, whose timezone is -6 
    # please change this accordingly, otherwise the program cannot be correct
    offset = (-6) * 3600

    down_ts = int((ts + offset)/86400) * 86400 - offset
    up_ts = down_ts + 86400

    return down_ts, up_ts
    # return timestamp_to_datetime(down_ts),timestamp_to_datetime(up_ts)

def time_round_day_datetime(date_str):
    # given a datetime, round the starting and ending timestamp of the day
    # "20200817-0600" =>  (1597644000, 1597730400)

    dtime = datetime.strptime(date_str, '%Y%m%d%z')
    timestamp = dtime.timestamp()
    return time_round_day(timestamp)

if __name__ == "__main__":
    print("Testing ...")
    # print(read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single_defined.txt"))
    # datetime_to_timestamp("2020-08-16 23:04:29.056")
    print(service_port_to_dict("service-names-port-numbers.csv"))