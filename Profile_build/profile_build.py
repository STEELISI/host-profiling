# Yebo Feng

import subprocess
import read_network as rn
import SubnetTree
import utilities as ut

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
    global profile_dict

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
        if prefix_flag == 1:
            add_outbound_record(start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes)
        if prefix_flag == 2:
            add_inbound_record(start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes)


def add_outbound_record(start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes):
    print("Outbound record added!")

def add_inbound_record(start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes):
    print("Inbound record added!")

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

if __name__ == "__main__":

    # initialize the profile dictionary
    global profile_dict
    profile_dict = dict()
    # initialize and read the prefix
    global nw_tree
    nw_tree = rn.read_build_tree()
    print("Successfully read the prefixes!")

    # read command 
    try:
        command = ut.read_command("/Users/yebof/Documents/host-profiling/Profile_build/NFDUMP_command/read_single_defined.txt")
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
        print("An exception occurred when inputting the NetFlow data!")
        print(e)
    
    # build profiles from the netflow data 
    profile_build(NF_input)