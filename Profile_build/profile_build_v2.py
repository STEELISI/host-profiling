# Yebo Feng

import profile
from ssl import PROTOCOL_TLS_SERVER
import subprocess
import read_network as rn
import SubnetTree
import utilities as ut
import time
import os
import argparse

# each profile is a dictionary
# {IP: dict()}
#
# each item in the sub_dict looks like:
#   For service-port-related:
#   "12:05-12:10|80": [12, 3000]
#       ^         ^     ^    ^
#       |         |     |    |
#      time      port  pkts  bytes
#
#   For non-service-port-related:
#   "12:05-12:10|0-100": [12, 3000]
#                 ^
#                 |
#        use a range to represent

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

        # protocol and tcp flag 
        prot = items[5].strip()
        tcp_flag = items[6].strip()
        # # test 
        # print('|'+prot+'|')
        # print('|'+tcp_flag+'|')

        pkts = int(items[7].strip())
        bytes = int(items[8].strip())
        # print(start_time, end_time, duration, pkts, bytes)

        # only keep TCP and UDP traffic 
        if prot != "17" and prot != "6":
            # print(record)
            continue

        # 1 if the first ip is in the prefixes but the second is not
        # 2 if the second ip is in the prefixes but the first is not
        # 0 if all the ips are in the prefixes or none of the ips are in the prefixes
        # we will skip case 0 
        prefix_flag = if_monitor(ip1, ip2)
        if prefix_flag == 0:
            continue
        elif prefix_flag == 2:
            # UDP flow from outside machine to FRGP machine - ignore. Not enough proof that that port is open.
            if prot == '17':
                continue
            if prot == '6':
                # TCP flow from outside machine to FRGP machine w PUSH or FIN - use, this is established connection. Remember that given port at FRGP is open
                if 'P' in tcp_flag or 'F' in tcp_flag:
                    update_record(prefix_flag, start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes)
                else:
                    continue
            else:
                update_record(prefix_flag, start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes)

        # Keep all the traffic from FRGP to outside 
        else:
            update_record(prefix_flag, start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes)


def update_record(direction_flag, start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes):
    global profile_dict
    global profile_date_down_ts
    global profile_date_up_ts

    # figure out the direction of the flow 
    if direction_flag == 1: # outbound
        profile_ip = ip1
        profile_port = ip1_port
        another_port = ip2_port
    else: # inbound
        profile_ip = ip2
        profile_port = ip2_port
        another_port = ip1_port

    if profile_ip not in profile_dict:
        # initialize the profile for ip1
        # 
        # each profile is a dictionary
        # {IP:[dict(), dict()]}
        # The first sub_dict is for outbound traffic
        # The second sub_dict is for inbound traffic 
        profile_dict[profile_ip] = dict()

    start_timestamp = ut.datetime_to_timestamp(start_time)
    end_timestamp = ut.datetime_to_timestamp(end_time)

    # the duration of flow is 0
    if duration == 0:
        if profile_date_down_ts <= start_timestamp < profile_date_up_ts:
            add_record_to_profile(direction_flag, start_timestamp, profile_ip, profile_port, another_port, pkts, bytes)
    
    
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
                add_record_to_profile(direction_flag, start_timestamp, profile_ip, profile_port, another_port, pkts, bytes)
        
        # cross two units 
        else:
            duration1 = end_s - start_timestamp
            # duration2 = duration - duration1
            pkts1 = (duration1/duration) * pkts
            pkts2 = pkts - pkts1
            bytes1 = (duration1/duration) * bytes
            bytes2 = bytes - bytes1
            if profile_date_down_ts < end_s <= profile_date_up_ts:
                add_record_to_profile(direction_flag, start_timestamp, profile_ip, profile_port, another_port, pkts1, bytes1)
            if profile_date_down_ts < end_e <= profile_date_up_ts:
                add_record_to_profile(direction_flag, end_timestamp, profile_ip, profile_port, another_port, pkts2, bytes2)
    
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
                add_record_to_profile(direction_flag, start_timestamp, profile_ip, profile_port, another_port, pkts1, bytes1)
        if profile_date_down_ts < end_e <= profile_date_up_ts:
                add_record_to_profile(direction_flag, end_timestamp, profile_ip, profile_port, another_port, pkts2, bytes2)
        if end_s != start_e:
            pkts_middle = (300/duration) * pkts
            bytes_middle = (300/duration) * bytes
            times = int((start_e-end_s)/300)
            position_time = end_s
            # print(times)
            for i in range(times):
                if profile_date_down_ts <= position_time < profile_date_up_ts:
                    add_record_to_profile(direction_flag, position_time, profile_ip, profile_port, another_port, pkts_middle,bytes_middle)
                position_time += 300


def add_record_to_profile(direction_flag, timestamp, ip, ip_port, another_port, pkts, bytes):
    # add the given information to the profile 
    global profile_dict
    start, end = time_mapping(timestamp)
    # record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(ip_port)

    # outbound traffic 
    if direction_flag == 1:
        if check_service_port(ip, ip_port, another_port) == 0:
        # if the first port is the service port, then return 1
        # if the second port is the service port, then return 2
        # if both ports are service ports, then treat the smaller port as the service port
        # if none of the ports are service ports, then return 0
            record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(ip_port, "out_from", "range")
        elif check_service_port(ip, ip_port, another_port) == 1:
            record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(ip_port, "out_from", "specific")
        elif check_service_port(ip, ip_port, another_port) == 2:
            record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(another_port, "out_to", "specific")
    # inbound traffic
    else:
        if check_service_port(ip, ip_port, another_port) == 0:
            record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(ip_port, "in_to", "range")
        elif check_service_port(ip, ip_port, another_port) == 1:
            record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(ip_port, "in_to", "specific")
        elif check_service_port(ip, ip_port, another_port) == 2:
            record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(another_port, "in_from", "specific")
    
    # print(ip+">"+record_key+">"+str(pkts)+">"+str(bytes))
    if record_key in profile_dict[ip]:
        temp = profile_dict[ip][record_key]
        profile_dict[ip][record_key] = [temp[0] + pkts, temp[1] + bytes]
    else:
        profile_dict[ip][record_key] = [pkts, bytes]

        # record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(another_port, check_service_port(another_port, ip_port))
        # if record_key in profile_dict[ip][0]:
        #     temp = profile_dict[ip][0][record_key]
        #     profile_dict[ip][0][record_key] = [temp[0] + pkts, temp[1] + bytes]
        # else:
        #     profile_dict[ip][0][record_key] = [pkts, bytes]

    # # inbound traffic
    # else:
    #     record_key = ut.timestamp_to_datetime(start) + "-" + ut.timestamp_to_datetime(end) + "|" + port_mapping_v1(ip_port, check_service_port(ip_port, another_port))
    #     if record_key in profile_dict[ip][1]:
    #         temp = profile_dict[ip][1][record_key]
    #         profile_dict[ip][1][record_key] = [temp[0] + pkts, temp[1] + bytes]
    #     else:
    #         profile_dict[ip][1][record_key] = [pkts, bytes]

def check_service_port(ip, port1, port2):
    # check which port is the service port 
    # 
    # if the first port is the service port, then return 1
    # if the second port is the service port, then return 2
    # if both ports are service ports, then treat the smaller port as the service port
    # if none of the ports are service ports, then return 0

    global service_ports_dict
    global port_usage_dict_for_IP

    if port1 in service_ports_dict:
        if port2 in service_ports_dict:
            # two ports all in service port dict
            if ip in port_usage_dict_for_IP:
                if port1 in port_usage_dict_for_IP[ip][0] and port2 in port_usage_dict_for_IP[ip][1]:
                    if port_usage_dict_for_IP[ip][0][port1][2] >  port_usage_dict_for_IP[ip][1][port2][2]:
                        return 1
                    elif port_usage_dict_for_IP[ip][0][port1][2] <  port_usage_dict_for_IP[ip][1][port2][2]:
                        return 2
                    elif float(port1) <= float(port2):
                        # if port1 != port2:
                        #     print("Equal!!!!!!!!!!!!")
                        #     print(ip+" "+port1+" "+port2)
                        
                        # only treats the smaller one as the service port 
                        return 1
                    else:
                        return 2
                elif float(port1) <= float(port2):
                    # only treats the smaller one as the service port 
                    print("outlier!!!!!!")
                    return 1
                else:
                    print("outlier!!!!!!")
                    return 2
            elif float(port1) <= float(port2):
                # only treats the smaller one as the service port 
                return 1
            else:
                return 2
        else:
            return 1
    else:
        if port2 in service_ports_dict:
            return 2
        else:
            # none of the ports are in service port dict 
            return 0


def port_mapping_v1(port, indicator, range_flag):
    # map the port number to a port range (string)
    # p_flag indicated whether the port is a service port 

    # 0 <= p < 1000 : every 100;
    # 1000 <= p < 10000: every 1000;
    # 10000 <= p < 50000: every 5000;
    # 50000 <= p: all.
    
    port_num = int(float(port))

    if range_flag == "specific":
        return indicator + "|" + port
    else:
        # 0-10000: 
        if port_num < 10000:
            # 0-1000: every 100 
            if port_num < 1000:
                down_num = int(port_num/100) * 100
                up_num = int(port_num/100) * 100 + 100
            # 1000-10000: every 1000
            else:
                down_num = int(port_num/1000) * 1000
                up_num = int(port_num/1000) * 1000 + 1000
        # 10000-:
        else:
            # 10000-50000: every 5000
            if port_num < 50000:
                down_num = int(port_num/5000) * 5000
                up_num = int(port_num/5000) * 5000 + 5000
            # 20000-:
            else:
                return indicator + "|" + "50000---"
        
        return indicator + "|" + str(down_num) + '---' + str(up_num)

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

def process_multiple_commands(netflow_path, profile_date_input, port_usage_for_each_ip_file, save_to_file):
    # which date the profile is
    global profile_date
    global profile_date_down_ts
    global profile_date_up_ts
    global service_ports_dict

    # load port usage dict (for each IP)
    print("Loading port usage dict (for each IP) ......")
    global port_usage_dict_for_IP
    this_dirname = os.path.dirname(__file__)
    port_usage_for_each_ip_filename = os.path.join(this_dirname, port_usage_for_each_ip_file)
    port_usage_dict_for_IP = ut.dict_read_from_file(port_usage_for_each_ip_filename)

    ####################
    # UPDATE THIS!!!
    ####################
    # profile_date = "20200817-0600"
    profile_date = profile_date_input
    profile_date_down_ts, profile_date_up_ts = ut.time_round_day_datetime(profile_date)
    service_ports_dict = ut.service_port_to_dict("service-names-port-numbers.csv")

    # initialize the profile dictionary
    global profile_dict
    profile_dict = dict()
    # initialize and read the prefix
    global nw_tree
    nw_tree = rn.read_build_tree()
    print("Successfully read the prefixes!")

    # files = ut.get_files('/Volumes/Laiky/FRGP_Netflow_ISI/validate/17')
    files = ut.get_files(netflow_path)

    # read command 
    try:
        # command = ut.read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single_defined.txt")
        # command = ut.read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single.txt")
        
        dirname = os.path.dirname(__file__)
        command_filename = os.path.join(dirname, 'NFDUMP_command/read_single.txt')

        command = ut.read_command(command_filename)
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
    ut.dict_write_to_file(profile_dict, save_to_file)

    # print(profile_dict)
    # TODO 

if __name__ == "__main__":
    # sample command: 
    # python3 profile_build_v2.py -p "/Volumes/Laiky/FRGP_Netflow_ISI/validate/17" -t "20200817-0600" -port_usage_for_each_endpoint "8.17_port_usage_for_each_endpoint.json" -r "results/8.17_profile_results_v2.txt"

    # process_multiple_commands()

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=str, required=True, help='The path of Netflow files. For example: \"/Volumes/Laiky/FRGP_Netflow_ISI/validate/17\".')
    parser.add_argument('-t', type=str, required=True, help='The time and timezone difference. For example: \"20200817-0600\".')
    parser.add_argument('-port_usage_for_each_endpoint', type=str, required=True, help='The path of dict with port usage for each endpoint. For example: \"8.17_port_usage_for_each_endpoint.json\".')
    parser.add_argument('-r', type=str, required=True, help='Which file should it save results to. For example: \"profile_results.txt\".')
    args = parser.parse_args()

    res_dirname = os.path.dirname(__file__)
    res_filename = os.path.join(res_dirname, args.r)
    
    process_multiple_commands(args.p, args.t, args.port_usage_for_each_endpoint, res_filename)