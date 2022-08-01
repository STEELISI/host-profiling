import subprocess
import read_network as rn
import SubnetTree
import utilities as ut
import profile_build as pb
import time

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
        prefix_flag = pb.if_monitor(ip1, ip2)
        if prefix_flag == 0:
            continue
        else:
            total_flow_number += 1
            total_packets += pkts
            total_bytes += bytes
            if (ip1 in service_ports_dict) or (ip2 in service_ports_dict):
                continue
            else:
                out_flow_number += 1
                out_packets += pkts
                out_bytes += bytes
    
    print("******************************")
    print("Proportion of flows out of the service port list: " + str(out_flow_number/total_flow_number))
    print("Proportion of packets out of the service port list: " + str(out_packets/total_packets))
    print("Proportion of bytes out of the service port list: " + str(out_bytes/total_bytes))
    print("******************************")



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


if __name__ == "__main__":
    measure_multiple()