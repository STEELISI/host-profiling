# Yebo Feng

import profile
import subprocess
import read_network as rn
import SubnetTree
import utilities as ut
import time

# each profile is a dictionary
# {IP:[dict(), dict()]}
# The first sub_dict is for outbound traffic
# The second sub_dict is for inbound traffic 

def if_monitor(ip1,ip2):
    # check whether one of the two IP addresses are within the defined prefixes 
    # return 1 if the first ip is in the prefixes but the second is not
    # return 2 if the second ip is in the prefixes but the first is not

    global nw_tree
    if ip1 in nw_tree:
        if ip2 not in nw_tree:
            return 1
    else:
        if ip2 in nw_tree:
            return 2
    return 0

def profile_build(flow_list):
    # global profile_dict

    for record in flow_list:
        # print(record)
        items = record.split("|")

        # ip1 is the source ip 
        # ip2 is the destination ip
        ip1_and_port = items[3].strip().split(":")
        ip2_and_port = items[4].strip().split(":")
        ip1 = ip1_and_port[0]
        ip1_port = ip1_and_port[1]
        ip2 = ip2_and_port[0]
        ip2_port = ip2_and_port[1]
        # print(ip1, ip1_port, ip2, ip2_port)
        start_time = items[0].strip()
        end_time = items[1].strip()
        duration = float(items[2].strip())
        pkts = int(items[7].strip())
        bytes = int(items[8].strip())
        # print(start_time, end_time, duration, pkts, bytes)

        # 1 if the first ip is in the prefixes but the second is not
        # 2 if the second ip is in the prefixes but the first is not
        # 0 if all the ips are in the prefixes or none of the ips are in the prefixes
        # we will skip case 0 
        prefix_flag = if_monitor(ip1, ip2)
        if prefix_flag == 0:
            continue
        else:
            update_record(prefix_flag, start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes)


def update_record(direction_flag, start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes):
    global profile_dict
    global profile_date_down_ts
    global profile_date_up_ts

    # figure out the direction of the flow 
    if direction_flag == 1:
        profile_ip = ip1
        profile_port = ip1_port
    else:
        profile_ip = ip2
        profile_port = ip2_port

    if profile_ip not in profile_dict:
        # initialize the profile for ip1
        # 
        # each profile is a dictionary
        # {IP:[dict(), dict()]}
        # The first sub_dict is for outbound traffic
        # The second sub_dict is for inbound traffic 
        profile_dict[profile_ip]=[dict(),dict()]

    start_timestamp = ut.datetime_to_timestamp(start_time)
    end_timestamp = ut.datetime_to_timestamp(end_time)

    # the duration of flow is 0
    if duration == 0:
        if profile_date_down_ts <= start_timestamp < profile_date_up_ts:
            add_record_to_profile(direction_flag, start_timestamp, profile_ip, profile_port, pkts, bytes)
    
    
    #       start_timestamp                                                      end_timestamp
    #             <-------------------------------------------------------------------> (flow)
    #             |-duration1-|                                         |--duration2--|
    #    |--------------------|--------------------|--------------------|--------------------|
    # start_s              end_s                                     start_e               end_e
    
    # the duration of flow is between 0 to 300
    # may cross two units 
    elif duration <= 300:
        start_s, end_s = time_mapping(start_timestamp)
        start_e, end_e = time_mapping(end_timestamp)

        # only within one unit 
        if start_s == start_e:
            if profile_date_down_ts <= start_timestamp < profile_date_up_ts:
                add_record_to_profile(direction_flag, start_timestamp, profile_ip, profile_port, pkts, bytes)
        
        # cross two units 
        else:
            duration1 = end_s - start_timestamp
            # duration2 = duration - duration1
            pkts1 = (duration1/duration) * pkts
            pkts2 = pkts - pkts1
            bytes1 = (duration1/duration) * bytes
            bytes2 = bytes - bytes1
            if profile_date_down_ts < end_s <= profile_date_up_ts:
                add_record_to_profile(direction_flag, start_timestamp, profile_ip, profile_port, pkts1, bytes1)
            if profile_date_down_ts < end_e <= profile_date_up_ts:
                add_record_to_profile(direction_flag, end_timestamp, profile_ip, profile_port, pkts2, bytes2)
    
    # cross more than two units 
    else:
        start_s, end_s = time_mapping(start_timestamp)
        start_e, end_e = time_mapping(end_timestamp)
        duration1 = end_s - start_timestamp
        duration2 = end_timestamp - start_e
        pkts1 = (duration1/duration) * pkts
        pkts2 = (duration2/duration) * pkts
        bytes1 = (duration1/duration) * bytes
        bytes2 = (duration2/duration) * bytes
        if profile_date_down_ts < end_s <= profile_date_up_ts:
                add_record_to_profile(direction_flag, start_timestamp, profile_ip, profile_port, pkts1, bytes1)
        if profile_date_down_ts < end_e <= profile_date_up_ts:
                add_record_to_profile(direction_flag, end_timestamp, profile_ip, profile_port, pkts2, bytes2)
        if end_s != start_e:
            pkts_middle = (300/duration) * pkts
            bytes_middle = (300/duration) * bytes
            times = int((start_e-end_s)/300)
            position_time = end_s
            # print(times)
            for i in range(times):
                if profile_date_down_ts <= position_time < profile_date_up_ts:
                    add_record_to_profile(direction_flag, position_time, profile_ip, profile_port, pkts_middle,bytes_middle)
                position_time += 300


def add_record_to_profile(direction_flag, timestamp, ip, ip_port, pkts, bytes):
    # add the given information to the profile 
    global profile_dict
    start, end = time_mapping(timestamp)
    record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(ip_port)

    # outbound traffic 
    if direction_flag == 1:
        if record_key in profile_dict[ip][0]:
            temp = profile_dict[ip][0][record_key]
            profile_dict[ip][0][record_key] = [temp[0] + pkts, temp[1] + bytes]
        else:
            profile_dict[ip][0][record_key] = [pkts, bytes]

    # inbound traffic
    else:
        if record_key in profile_dict[ip][1]:
            temp = profile_dict[ip][1][record_key]
            profile_dict[ip][1][record_key] = [temp[0] + pkts, temp[1] + bytes]
        else:
            profile_dict[ip][1][record_key] = [pkts, bytes]


def port_mapping_v1(port):
    # map the port number to a port range (string)

    # 0 <= p < 200 : every 10;
    # 200 <= p < 1000: every 100;
    # 1000 <= p < 16000: every 1000;
    # 16000 <= p < 20000: every 2000;
    # 20000 <= p: all.

    global service_ports_dict
    if port in service_ports_dict:
        return port
    
    port_num = int(float(port))

    # 0-1000: 
    if port_num < 1000:
        # 0-200: 
        if port_num < 200:
            down_num = int(port_num/10) * 10
            up_num = int(port_num/10) * 10 + 10
        # 200-1000: 
        else:
            down_num = int(port_num/100) * 100
            up_num = int(port_num/100) * 100 + 100
    # 1000-:
    else:
        # 1000-16000:
        if port_num < 16000:
            down_num = int(port_num/1000) * 1000
            up_num = int(port_num/1000) * 1000 + 1000
        # 16000-20000:
        elif port_num < 20000:
            down_num = int(port_num/2000) * 2000
            up_num = int(port_num/2000) * 2000 + 2000
        # 20000-:
        else:
            return "20000-"

    return str(down_num)+'-'+str(up_num)

def time_mapping(time_input):
    # map the timestamp to 5 minutes (300s) round 

    down_time = int(time_input/300) * 300
    up_time = int(time_input/300) * 300 + 300

    # return two integers
    return down_time,up_time

def run_bash(command,opt):
    # take a command, run it, and get the output 

    # simple output 
    if opt == 1:
        commands = command.split(' ')
        result = subprocess.run(commands, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').strip()

    # complicated output 
    if opt == 2:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        return output.decode('utf-8').strip()

def process_single_command():

    # which date the profile is
    global profile_date
    global profile_date_down_ts
    global profile_date_up_ts  
    profile_date = "20200817-0600"
    profile_date_down_ts, profile_date_up_ts = ut.time_round_day_datetime(profile_date)

    # initialize the profile dictionary
    global profile_dict
    profile_dict = dict()
    # initialize and read the prefix
    global nw_tree
    nw_tree = rn.read_build_tree()
    print("Successfully read the prefixes!")

    # read command 
    try:
        # command = ut.read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single_defined.txt")
        command = ut.read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single.txt")
        command = ' '.join(command)
        print("Successfully read the command:")
        print("\t"+command)
    except Exception as e:
        print("An exception occurred when reading the command!")
        print(e)

    # run the command and read the Netflow data
    try:
        print("Inputting the NetFlow data now...")
        # run with opt 2 as it is complicated output 
        NF_input = run_bash(command,2)
        NF_input = NF_input.strip().split("\n")
        print("NetFlow input successfully!")
    except Exception as e:
        print("An exception occurred when building profiles from the NetFlow data!")
        print(e)
    
    # build profiles from the netflow data 
    profile_build(NF_input)

    # print(profile_dict)
    # TODO 

def process_multiple_commands():
    # which date the profile is
    global profile_date
    global profile_date_down_ts
    global profile_date_up_ts
    global service_ports_dict

    ####################
    # UPDATE THIS!!!
    ####################
    profile_date = "20200817-0600"
    profile_date_down_ts, profile_date_up_ts = ut.time_round_day_datetime(profile_date)
    service_ports_dict = ut.service_port_to_dict("service-names-port-numbers.csv")

    # initialize the profile dictionary
    global profile_dict
    profile_dict = dict()
    # initialize and read the prefix
    global nw_tree
    nw_tree = rn.read_build_tree()
    print("Successfully read the prefixes!")

    files = ut.get_files('/Volumes/Laiky/FRGP_Netflow_ISI/validate/17')

    # read command 
    try:
        # command = ut.read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single_defined.txt")
        command = ut.read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single.txt")
        # command = ' '.join(command)
        print("Successfully read the command:")
        print("\t"+' '.join(command))
    except Exception as e:
        print("An exception occurred when reading the command!")
        print(e)

    # run the command and read the Netflow data
    profile_build_start_time = time.time()

    try:
        for file in files:
            runtime_start = time.time()
            print("Inputting the 5 mins of NetFlow data now...")
            print(file)
            command[2] = file

            # run with opt 2 as it is complicated output 
            NF_input = run_bash(' '.join(command),2)
            NF_input = NF_input.strip().split("\n")
            print("NetFlow input successfully!")

            # build profiles from the netflow data 
            profile_build(NF_input)
            runtime_end = time.time()
            runtime = float(runtime_end - runtime_start)

            print("~"*10 + " Profiles built for " + file + " " + "~"*10)
            print("~"*10 + " Toke " + str(runtime) +"s " + "~"*10)
    except Exception as e:
        print("An exception occurred when building profiles from the NetFlow data!")
        print(e)
    
    profile_build_end_time = time.time()
    profile_build_time_taken = profile_build_end_time - profile_build_start_time

    print("Everything completed!")
    print("Toke " + str(profile_build_time_taken) + " s.")
    ut.dict_write_to_file(profile_dict,"results.txt")

    # print(profile_dict)
    # TODO 

if __name__ == "__main__":
    # process_single_command()
    process_multiple_commands()