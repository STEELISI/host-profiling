# Yebo Feng 
import profile
import profile_build as pb
import utilities as ut
from itertools import islice

def profile_dict_to_list_v1(profile_dict):
    #########################################
    #########################################
    # if port_num < 1000:
    #     # 0-200: 20
    #     if port_num < 200:
    #         down_num = int(port_num/10) * 10
    #         up_num = int(port_num/10) * 10 + 10
    #     # 200-1000: 8
    #     else:
    #         down_num = int(port_num/100) * 100
    #         up_num = int(port_num/100) * 100 + 100
    # # 1000-:
    # else:
    #     # 1000-16000: 15
    #     if port_num < 16000:
    #         down_num = int(port_num/1000) * 1000
    #         up_num = int(port_num/1000) * 1000 + 1000
    #     # 16000-20000: 2
    #     elif port_num < 20000:
    #         down_num = int(port_num/2000) * 2000
    #         up_num = int(port_num/2000) * 2000 + 2000
    #     # 20000-: 1
    #     else:
    #         return "20000-"
    #########################################
    #########################################

    # initialize
    inbound = [[[0,0]] * 46] * 288
    outbound = [[[0,0]] * 46] * 288

    # TODO 
    return inbound, outbound

def print_nth_profile(file,num):
    # print the nth element in the profile dictionary
    
    pf_dict = ut.dict_read_from_file(file)

    it = iter(pf_dict)
    # Consume n elements.
    next(islice(it, num, num), None) 
    # Return the value at the current position.
    # This raises StopIteration if n is beyond the limits.
    # Use next(it, None) to suppress that exception.
    item = next(it)

    print(item)
    print(pf_dict[item])

def print_n_profiles(file,num):
    # print the first n elements in the profile dictionary
    
    pf_dict = ut.dict_read_from_file(file)

    it = iter(pf_dict)

    for i in range(num):
        dict_key = next(it)
        print(str(dict_key) + "; " + str(pf_dict[dict_key]))
        print("=========================================")

def extract_service_ports(file1, file2):
    # read the profile and build a dictionary according to the service ports 
    #
    # file1 is the profile
    # file2 is the file to save the results

    service_ports_dict = ut.service_port_to_dict("service-names-port-numbers.csv")
    pf_dict = ut.dict_read_from_file(file1)
    clustering_dict = {}

    print("Analyzing the profiles...")
    # enumerate the profile dictionary 
    for i, (k, v) in enumerate(pf_dict.items()):
        temp_res = [dict(),dict()]
        outbound_dict = v[0]
        inbound_dict = v[1]

        # process the outbound ports
        for j, (k_out, v_out) in enumerate(outbound_dict.items()):
            index_list = k_out.split("|")
            port = index_list[1]
            if "-" in port:
                continue
            else:
                temp_res[0][port] = service_ports_dict[port]
        
        # process the inbound ports
        for j, (k_in, v_in) in enumerate(inbound_dict.items()):
            index_list = k_in.split("|")
            port = index_list[1]
            if "-" in port:
                continue
            else:
                temp_res[1][port] = service_ports_dict[port]

        clustering_dict[k] = temp_res
    
    ut.dict_write_to_file(clustering_dict, file2)

def extract_most_used_service_ports(num , file1, file2):
    # read the profile and build a dictionary according to the most used service ports 
    #
    # num indicates the top num service ports
    # file1 is the profile
    # file2 is the file to save the results

    service_ports_dict = ut.service_port_to_dict("service-names-port-numbers.csv")
    pf_dict = ut.dict_read_from_file(file1)
    clustering_dict = {}


if __name__ == "__main__":
    print("running")

    # # print the nth profile 
    # print_nth_profile("results_v2.txt",12)

    # # print the first n profiles
    # print_n_profiles("results_v2.txt",12)
    
    # # Clustering
    # extract_service_ports("results_v2.txt", "clustering_results.txt")

    # print the first n clustering results
    print_n_profiles("clustering_results.txt",20)