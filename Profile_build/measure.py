import profile
import subprocess
import read_network as rn
import SubnetTree
import utilities as ut
import profile_build as pb
import time
import os
import argparse
import read_network as rn

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

def measure_traffic_out_service(flow_list):

    global service_ports_dict

    global total_flow_number
    global total_packets
    global total_bytes 

    global out_flow_number
    global out_packets
    global out_bytes 

    for record in flow_list:
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
            total_flow_number += 1
            total_packets += pkts
            total_bytes += bytes
            if (ip1_port in service_ports_dict) or (ip2_port in service_ports_dict):
                continue
            else:
                out_flow_number += 1
                out_packets += pkts
                out_bytes += bytes
                print(record)
    
    print("******************************")
    print("Proportion of flows out of the service port list: " + str(out_flow_number/total_flow_number))
    print("Proportion of packets out of the service port list: " + str(out_packets/total_packets))
    print("Proportion of bytes out of the service port list: " + str(out_bytes/total_bytes))
    print("******************************")


def port_usage_count(flow_list):
    # count the usage of ports that are in the service port list 
    global service_ports_dict
    global port_usage_dict

    for record in flow_list:
        items = record.split("|")
        # ip1 is the source ip 
        # ip2 is the destination ip
        ip1_and_port = items[3].strip().split(":")
        ip2_and_port = items[4].strip().split(":")
        ip1_port = ip1_and_port[1]
        ip2_port = ip2_and_port[1]
        pkts = int(items[7].strip())
        bytes = int(items[8].strip())

        # update the usage information if the port is in the service port list
        # do this for all two ports
        if ip1_port in service_ports_dict:
            if ip1_port in port_usage_dict:
                temp_pkts = port_usage_dict[ip1_port][0]
                temp_bytes = port_usage_dict[ip1_port][1]
                port_usage_dict[ip1_port][0] = temp_pkts + pkts
                port_usage_dict[ip1_port][1] = temp_bytes + bytes
            else:
                port_usage_dict[ip1_port] = [pkts, bytes]
            # print(port_usage_dict[ip1_port])
        
        if ip2_port in service_ports_dict:
            if ip2_port in port_usage_dict:
                temp_pkts = port_usage_dict[ip2_port][0]
                temp_bytes = port_usage_dict[ip2_port][1]
                port_usage_dict[ip2_port][0] = temp_pkts + pkts
                port_usage_dict[ip2_port][1] = temp_bytes + bytes
            else:
                port_usage_dict[ip2_port] = [pkts, bytes]
            # print(port_usage_dict[ip2_port])

def port_usage_count_for_each_IP(flow_list):
    # global port_usage_dict_for_IP

    for record in flow_list:
        items = record.split("|")

        # ip1 is the source ip 
        # ip2 is the destination ip
        ip1_and_port = items[3].strip().split(":")
        ip2_and_port = items[4].strip().split(":")
        ip1 = ip1_and_port[0]
        ip1_port = ip1_and_port[1]
        ip2 = ip2_and_port[0]
        ip2_port = ip2_and_port[1]
        prot = items[5].strip()
        tcp_flag = items[6].strip()
        # print(ip1, ip1_port, ip2, ip2_port)
        pkts = int(items[7].strip())
        bytes = int(items[8].strip())

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
        elif prefix_flag == 2: # 2 if the second ip is in the prefixes but the first is not
            # UDP flow from outside machine to FRGP machine - ignore. Not enough proof that that port is open.
            if prot == '17':
                continue
            if prot == '6':
                # TCP flow from outside machine to FRGP machine w PUSH or FIN - use, this is established connection. Remember that given port at FRGP is open
                if 'P' in tcp_flag or 'F' in tcp_flag:
                    update_port_usage_for_each_endpoint(ip2, ip2_port, ip1_port, pkts, bytes)
                else:
                    continue
        # Keep all the traffic from FRGP to outside 
        else: # 1 if the first ip is in the prefixes but the second is not
            update_port_usage_for_each_endpoint(ip1, ip1_port, ip2_port, pkts, bytes)
        

def update_port_usage_for_each_endpoint(IP, internal_port, remote_port, pkts, bytes):
    global port_usage_dict_for_IP

    if IP not in port_usage_dict_for_IP:
        port_usage_dict_for_IP[IP] = [{},{}]
    
    # update for internal port 
    if internal_port in port_usage_dict_for_IP[IP][0]:
        temp = port_usage_dict_for_IP[IP][0][internal_port]
        port_usage_dict_for_IP[IP][0][internal_port] = [temp[0] + 1, temp[1] + pkts, temp[2] + bytes]
    else:
        port_usage_dict_for_IP[IP][0][internal_port] = [1, pkts, bytes]
    
    # update for external port 
    if remote_port in port_usage_dict_for_IP[IP][1]:
        temp2 = port_usage_dict_for_IP[IP][1][remote_port]
        port_usage_dict_for_IP[IP][1][remote_port] = [temp2[0] + 1, temp2[1] + pkts, temp2[2] + bytes]
    else:
        port_usage_dict_for_IP[IP][1][remote_port] = [1, pkts, bytes]

def measure_port_usage_for_each_ip(path_of_files, save_to_file):
    # Count the port usage for each endpoint separately. 

    # read service ports 
    global service_ports_dict
    service_ports_dict = ut.service_port_to_dict("service-names-port-numbers.csv")
    # initialize and read the prefix
    global nw_tree
    nw_tree = rn.read_build_tree()
    print("Successfully read the prefixes!")

    # initialize the dict to store the results (port usage for each endpoint)
    global port_usage_dict_for_IP
    port_usage_dict_for_IP = {}
    # {IP:[{},{}]}
    # The first sub dict {internal_port:[flow_num, pkts, bytes]}
    # The second sub dict {remote_port:[flow_num, pkts, bytes]}

    files = ut.get_files(path_of_files)

    # read command 
    try:
        dirname = os.path.dirname(__file__)
        command_filename = os.path.join(dirname, "NFDUMP_command/read_single.txt")
        command = ut.read_command(command_filename)
        # command = ' '.join(command)
        print("Successfully read the command:")
        print("\t"+' '.join(command))
    except Exception as e:
        print("An exception occurred when reading the command!")
        print(e)
    
    # run the command and read the Netflow data
    measure_start_time = time.time()

    try:
        for file in files:
            runtime_start = time.time()
            print("Inputting the 5 mins of NetFlow data now...")
            print(file)
            command[2] = file

            # run with opt 2 as it is complicated output 
            NF_input = pb.run_bash(' '.join(command),2)
            NF_input = NF_input.strip().split("\n")
            print("NetFlow input successfully!")

            # build profiles from the netflow data 
            port_usage_count_for_each_IP(NF_input)
            runtime_end = time.time()
            runtime = float(runtime_end - runtime_start)

            print("~"*10 + " Port usage counted for " + file + " " + "~"*10)
            print("~"*10 + " Toke " + str(runtime) +"s " + "~"*10)
    except Exception as e:
        print("An exception occurred when building profiles from the NetFlow data!")
        print(e)

    # save file
    the_dirname = os.path.dirname(__file__)
    save_to_filename = os.path.join(the_dirname, save_to_file)
    ut.dict_write_to_file(port_usage_dict_for_IP, save_to_filename)
    
    measure_end_time = time.time()
    measure_time_taken = measure_end_time - measure_start_time
    print("Total time taken: " + str(measure_time_taken) + "s.")

def measure_port_usage(path_of_files):
    # Count the port usage for all flows in the Netflow (not for each endpoint separately). 

    # read service ports 
    global service_ports_dict
    service_ports_dict = ut.service_port_to_dict("service-names-port-numbers.csv")

    global port_usage_dict
    port_usage_dict = {}

    files = ut.get_files(path_of_files)

    # read command 
    try:
        dirname = os.path.dirname(__file__)
        command_filename = os.path.join(dirname, "NFDUMP_command/read_single.txt")
        command = ut.read_command(command_filename)
        # command = ' '.join(command)
        print("Successfully read the command:")
        print("\t"+' '.join(command))
    except Exception as e:
        print("An exception occurred when reading the command!")
        print(e)

    # run the command and read the Netflow data
    measure_start_time = time.time()

    try:
        for file in files:
            runtime_start = time.time()
            print("Inputting the 5 mins of NetFlow data now...")
            print(file)
            command[2] = file

            # run with opt 2 as it is complicated output 
            NF_input = pb.run_bash(' '.join(command),2)
            NF_input = NF_input.strip().split("\n")
            print("NetFlow input successfully!")

            # build profiles from the netflow data 
            port_usage_count(NF_input)
            runtime_end = time.time()
            runtime = float(runtime_end - runtime_start)

            print("~"*10 + " Port usage counted for " + file + " " + "~"*10)
            print("~"*10 + " Toke " + str(runtime) +"s " + "~"*10)
    except Exception as e:
        print("An exception occurred when building profiles from the NetFlow data!")
        print(e)

    print("Start converting to a list and sorting.")
    port_usage_list = list(port_usage_dict.items())
    # sort from large to small 
    def sort_key1(e):
        # return bytes 
        return int(e[1][1])
    port_usage_list.sort(reverse = True, key = sort_key1)

    # save file 
    ut.save_port_usage_to_file(port_usage_list, "service_port_usage_rank.csv")
    
    measure_end_time = time.time()
    measure_time_taken = measure_end_time - measure_start_time
    print("Total time taken: " + str(measure_time_taken) + "s.")

def measure_continuous_ip(file1, file2):
    print("Loading all the files......")
    dirname = os.path.dirname(__file__)
    ip_file_1 = os.path.join(dirname, file1)
    ip_file_2 = os.path.join(dirname, file2)

    ip_list_1 = ut.read_list_from_file_linebyline(ip_file_1)
    ip_list_2 = ut.read_list_from_file_linebyline(ip_file_2)

    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    print("The size of the first list: " + str(len(ip_list_1)))
    print("The size of the second list: " + str(len(ip_list_2)))
    print("Number of common ips: " + str(len(intersection(ip_list_1, ip_list_2))))

def measure_multiple():
    global service_ports_dict
    service_ports_dict = ut.service_port_to_dict("service-names-port-numbers.csv")

    # initialize and read the prefix
    global nw_tree
    nw_tree = rn.read_build_tree()
    print("Successfully read the prefixes!")

    global total_flow_number
    total_flow_number = 0
    global total_packets
    total_packets = 0
    global total_bytes 
    total_bytes = 0

    global out_flow_number
    out_flow_number = 0
    global out_packets
    out_packets = 0
    global out_bytes 
    out_bytes = 0

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
    measure_start_time = time.time()

    try:
        for file in files:
            runtime_start = time.time()
            print("Inputting the 5 mins of NetFlow data now...")
            print(file)
            command[2] = file

            # run with opt 2 as it is complicated output 
            NF_input = pb.run_bash(' '.join(command),2)
            NF_input = NF_input.strip().split("\n")
            print("NetFlow input successfully!")

            # build profiles from the netflow data 
            measure_traffic_out_service(NF_input)
            runtime_end = time.time()
            runtime = float(runtime_end - runtime_start)

            print("~"*10 + " Profiles built for " + file + " " + "~"*10)
            print("~"*10 + " Toke " + str(runtime) +"s " + "~"*10)
    except Exception as e:
        print("An exception occurred when building profiles from the NetFlow data!")
        print(e)
    
    measure_end_time = time.time()
    measure_time_taken = measure_end_time - measure_start_time

def number_of_items_in_dict(filename):
    # how many items are there in the dict? 
    print(len(ut.dict_read_from_file(filename)))

if __name__ == "__main__":
    # python3 measure.py -mpufa "/Volumes/Laiky/FRGP_Netflow_ISI/validate/17"
    # python3 measure.py -port_usage_for_each_endpoint "/Volumes/Laiky/FRGP_Netflow_ISI/validate/17" -save_to "8.17_port_usage_for_each_endpoint.json"
    # python3 measure.py -cont1 8.17_unrestricted_v2.txt -cont2 8.18_unrestricted_v2.txt

    # measure_multiple()
    # number_of_items_in_dict("profile_results.txt")

    parser = argparse.ArgumentParser()
    parser.add_argument('-mpufa', type=str, help='Count the port usage for all flows in the Netflow (not for each endpoint separately). Enter the path of Netflow, For example: \"/Volumes/Laiky/FRGP_Netflow_ISI/validate/17\".')
    parser.add_argument('-port_usage_for_each_endpoint', type=str, help="Count the port usage for each endpoint separately. Enter the path of Netflow, For example: \"/Volumes/Laiky/FRGP_Netflow_ISI/validate/17\".")
    parser.add_argument('-save_to', type=str, help="Save the result to. For example: \"/8.17_port_usage_for_each_endpoint.json\".")
    parser.add_argument('-cont1', type=str, help="The first file for IP list (for measuring common IPs). For example: \"/8.17_restricted_ip.txt\".")
    parser.add_argument('-cont2', type=str, help="The second file for IP list (for measuring common IPs). For example: \"/8.18_restricted_ip.txt\".")
    args = parser.parse_args()

    if args.mpufa:
        measure_port_usage(args.mpufa)
    elif args.port_usage_for_each_endpoint and args.save_to:
        measure_port_usage_for_each_ip(args.port_usage_for_each_endpoint, args.save_to)
    elif args.cont1:
        measure_continuous_ip(args.cont1, args.cont2)