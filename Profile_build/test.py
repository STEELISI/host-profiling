import profile_build as pb
import utilities as ut
from datetime import datetime
import json
import time

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
    ut.dict_write_to_file(details, "pf.txt")

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

if __name__ == "__main__":
    print("Testing ...")
    # test_time_mapping()
    # test_dict_write()
    # test_dict_read()
    test_dict_read("results.txt")