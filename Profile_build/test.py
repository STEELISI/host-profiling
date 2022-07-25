import profile_build as pb
import utilities as ut
from datetime import datetime
import json

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
    details = {'Name': "Bob", 'Age' :28, 'name2':{'a':1,'b':2}}
    with open('dict.txt', 'w') as convert_file:
        convert_file.write(json.dumps(details))

if __name__ == "__main__":
    print("Testing ...")
    # test_time_mapping()
    test_dict_write()