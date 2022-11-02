import argparse
import copy
import utilities as ut
import os
import time
import gc

def merge(path, start, end, save_to):
    # initialize the dict to store the results (port usage for each endpoint)
    global port_usage_dict_for_IP
    port_usage_dict_for_IP = {}
    # {IP:[{},{}]}
    # The first sub dict {internal_port:[flow_num, pkts, bytes]}
    # The second sub dict {remote_port:[flow_num, pkts, bytes]}

    all_files = ut.get_all_files(path)
    files = []
    for i in all_files:
        if "port_usage_for_each" in i:
            date = int(i.split('/')[-1].split('_')[0].split('.')[1])
            if date <= end and date >= start:
                files.append(i)
    
    measure_start_time = time.time()
    
    for file in files:
        runtime_start = time.time()
        print("Starting file " + file + " now...")

        new_dict = ut.dict_read_from_file(file)
        for num, (k, v) in enumerate(new_dict.items()):
            if k not in port_usage_dict_for_IP:
                port_usage_dict_for_IP[k] = copy.deepcopy(v)
            else:
                # k in port_usage_dict_for_IP
                internal_dict = v[0]
                remote_dict = v[1]

                # for internal ports 
                for num1, (k1, v1) in enumerate(internal_dict.items()):
                    if k1 not in port_usage_dict_for_IP[k][0]:
                        port_usage_dict_for_IP[k][0][k1] = copy.deepcopy(v1)
                    else:
                        flow_num_old = port_usage_dict_for_IP[k][0][k1][0]
                        pkts_old = port_usage_dict_for_IP[k][0][k1][1]
                        bytes_old = port_usage_dict_for_IP[k][0][k1][2]

                        flow_num_new = v1[0]
                        pkts_new = v1[1]
                        bytes_new = v1[2]

                        port_usage_dict_for_IP[k][0][k1][0] = flow_num_old + flow_num_new
                        port_usage_dict_for_IP[k][0][k1][1] = pkts_old + pkts_new
                        port_usage_dict_for_IP[k][0][k1][2] = bytes_old + bytes_new
                
                del internal_dict
                
                # for remote ports 
                for num2, (k2, v2) in enumerate(remote_dict.items()):
                    if k2 not in port_usage_dict_for_IP[k][1]:
                        port_usage_dict_for_IP[k][1][k2] = copy.deepcopy(v2)
                    else:
                        flow_num_old = port_usage_dict_for_IP[k][1][k2][0]
                        pkts_old = port_usage_dict_for_IP[k][1][k2][1]
                        bytes_old = port_usage_dict_for_IP[k][1][k2][2]

                        flow_num_new = v2[0]
                        pkts_new = v2[1]
                        bytes_new = v2[2]

                        port_usage_dict_for_IP[k][1][k2][0] = flow_num_old + flow_num_new
                        port_usage_dict_for_IP[k][1][k2][1] = pkts_old + pkts_new
                        port_usage_dict_for_IP[k][1][k2][2] = bytes_old + bytes_new
                
                del remote_dict
        
        del new_dict
        
        runtime_end = time.time()
        runtime = float(runtime_end - runtime_start)
        print("~"*10 + " Toke " + str(runtime) +"s " + "~"*10)
    
    # save file
    print("Saving file to " + save_to + " now ......")
    the_dirname = os.path.dirname(__file__)
    save_to_filename = os.path.join(the_dirname, save_to)
    ut.dict_write_to_file(port_usage_dict_for_IP, save_to_filename)

    measure_end_time = time.time()
    measure_time_taken = measure_end_time - measure_start_time
    print("Total time taken: " + str(measure_time_taken) + "s.")


if __name__ == "__main__":
    # python3 merge_port_usage.py -path "/Users/yebof/Documents/host-profiling/Profile_build/results" -start 17 -end 23 -save_to "8.17-8.23_port_usage_for_each_endpoint_multiple.json"
    # python3 merge_port_usage.py -path "/Users/yebof/Documents/host-profiling/Profile_build/results" -start 24 -end 30 -save_to "8.24-8.30_port_usage_for_each_endpoint_multiple.json"

    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=str, help='The path that stores the port usage info, For example: \"/Volumes/Laiky/FRGP_Netflow_ISI/validate/17\".')
    parser.add_argument('-start', type=int, help='Start date. For example 17.')
    parser.add_argument('-end', type=int, help='End date. For example 23.')
    parser.add_argument('-save_to', type=str, help="Save the result to. For example: \"/8.17_port_usage_for_each_endpoint.json\".")
    args = parser.parse_args()

    if args.path and args.start and args.end and args.save_to:
        merge(args.path, args.start, args.end, args.save_to)
