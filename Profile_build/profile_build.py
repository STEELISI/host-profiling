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
    # global profile_dict

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
            update_outbound_record(start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes)
        if prefix_flag == 2:
            update_inbound_record(start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes)


def update_outbound_record(start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes):
    global profile_dict
    if ip1 not in profile_dict:
        # initialize the profile for ip1
        # 
        # each profile is a dictionary
        # {IP:[dict(), dict()]}
        # The first sub_dict is for outbound traffic
        # The second sub_dict is for inbound traffic 
        profile_build[ip1]=[dict(),dict()]

    print("Outbound record added!")

def update_inbound_record(start_time, end_time, duration, ip1, ip1_port, ip2, ip2_port, pkts, bytes):
    global profile_dict
    if ip2 not in profile_dict:
        # initialize the profile for ip1
        # 
        # each profile is a dictionary
        # {IP:[dict(), dict()]}
        # The first sub_dict is for outbound traffic
        # The second sub_dict is for inbound traffic 
        profile_build[ip2]=[dict(),dict()]

    print("Inbound record added!")

def port_mapping(port):
    # map the port number to a port range

    # 0 <= p < 200 : every 10;
    # 200 <= p < 1000: every 100;
    # 1000 <= p < 16000: every 1000;
    # 16000 <= p < 20000: every 2000;
    # 20000 <= p: all.

    port_num = int(port)

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