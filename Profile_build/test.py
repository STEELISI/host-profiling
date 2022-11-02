import profile_build as pb
import utilities as ut
from datetime import datetime
import json
import time
import os

def test_port_mapping():
    print(pb.port_mapping("0") + " should be 0-10")
    print(pb.port_mapping("3") + " should be 0-10")
    print(pb.port_mapping("5") + " should be 0-10")
    print(pb.port_mapping("8") + " should be 0-10")
    print(pb.port_mapping("23") + " should be 20-30")
    print(pb.port_mapping("123") + " should be 120-130")
    print(pb.port_mapping("80") + " should be 80-90")
    print(pb.port_mapping("8080") + " should be 8000-9000")
    print(pb.port_mapping("28080") + " should be 20000-")
    print(pb.port_mapping("19080") + " should be 18000-20000")
    print(pb.port_mapping("3306") + " should be 3000-4000")

def test_port_mapping_v1():
    print(pb.port_mapping_v1("0",2) + " should be 0-10")
    print(pb.port_mapping_v1("3",2) + " should be 0-10")
    print(pb.port_mapping_v1("5",2) + " should be 0-10")
    print(pb.port_mapping_v1("8",2) + " should be 0-10")
    print(pb.port_mapping_v1("23",2) + " should be 20-30")
    print(pb.port_mapping_v1("123",2) + " should be 120-130")
    print(pb.port_mapping_v1("80",2) + " should be 80-90")
    print(pb.port_mapping_v1("8080",2) + " should be 8000-9000")
    print(pb.port_mapping_v1("28080",2) + " should be 20000-")
    print(pb.port_mapping_v1("19080",2) + " should be 18000-20000")
    print(pb.port_mapping_v1("3306",2) + " should be 3000-4000")

def test_time_mapping():
    print(pb.time_mapping(ut.datetime_to_timestamp("2020-08-16 23:04:29.056")))
    print(ut.timestamp_to_datetime(1597644269.056))
    print(ut.timestamp_to_datetime(1597644000))
    print(ut.timestamp_to_datetime(1597644300))
    print(ut.time_round_day(1597644269.056))
    print("="*20)
    print(ut.time_round_day_datetime("20200818-0600"))

def test_dict_write():
    details = {'Name': "Bob", 'Age' :28, 'name2':{'a':[{"a1":3},{"a2":3},{}],'b':2}}
    # a = set()
    # a.add("hi")
    ut.dict_write_to_file(a, "test.txt")

def test_dict_read():
    test_dict_write()
    dict = ut.dict_read_from_file("pf.txt")
    print("Type:", type(dict))
    print(dict)
    print(dict["Age"])
    print(dict["name2"])
    print(dict["name2"]["a"])

def test_dict_read(f):
    dict_read_start_time = time.time()
    dict = ut.dict_read_from_file(f)
    dict_read_end_time = time.time()
    dict_read_time_taken = dict_read_end_time - dict_read_start_time
    print("Toke " + str(dict_read_time_taken) + " s.")

    print(len(dict))

def test_relative_path():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'results/')
    print(filename)

def file_path(f):
    res_dirname = os.path.dirname(__file__)
    res_filename = os.path.join(res_dirname, f)
    print(res_filename)

def get_folders(folder):
    subfolders = [ f.path for f in os.scandir(folder) if f.is_dir() ]
    print(subfolders)
    target_folders = []
    for i in subfolders:
        if int(i.split("/")[-1]) >= 21 and int(i.split("/")[-1]) <= 27:
            target_folders.append(i)
    print(target_folders)

def test_path(netflow_path, start = 17, end = 23):
    # fetch pathes of all the netflow files 
    all_folders = ut.get_folders(netflow_path)
    # fetch all the folders 
    folders = []
    for i in all_folders:
        folder_date = int(i.split('/')[-1])
        if folder_date >= start and folder_date <= end:
            folders.append(i)
    files = []
    # fetch all the files in all the selected folders 
    for i in folders:
        files = files + ut.get_files(i)
    print(files)

def test_time(profile_date, start=17, end=23):
    profile_date_down_ts, profile_date_up_ts = ut.time_round_day_datetime(profile_date)
    print(profile_date_down_ts, profile_date_up_ts)

if __name__ == "__main__":
    print("Testing ...")
    # test_time_mapping()
    # test_dict_write()
    # test_dict_read()
    # test_dict_read("results.txt")
    # test_port_mapping_v1()
    # test_relative_path()
    # file_path("../")
    # get_folders("/Volumes/Laiky/FRGP_Netflow_ISI/validate/")
    # test_path("/Volumes/Laiky/FRGP_Netflow_ISI/validate/")
    test_time("20200817-0600")