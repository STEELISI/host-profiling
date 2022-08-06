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
        print(">>>>>>>>>> " + str(dict_key) + " <<<<<<<<<<")
        for i in pf_dict[dict_key]:
            print("=========================================")
            print(str(i))
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

def simplified_profile_generation(num , file1, file2):
    # read the profile and build a dictionary according to the most used service ports 
    #
    # num indicates the top num service ports
    # file1 is the profile
    # file2 is the file to save the results
    #
    # Layout of the simplified profile:
    # {"IP 1": [item1, item2, item3], "IP 2": [item1, item2, item3], ......}
    #           item1: the topic of this IP address,
    #                  a sorted list with up to 10 items [["Inbound|80|http", 0.5, 0.5], ["Inbound|---|NON_SERVICE_PORT", 0.3, 0.25], ......]
    #                                                                          ^    ^
    #                                                                          |    |
    #                                                          proportion of pkts   proportion of bytes
    #           item2: the traffic throughput of this IP address, a list
    #                   [item1, item2, item3, item4]
    #                   item1: outbound pkts total, item2: outbound bytes total
    #                   item3: outbound pkts total, item4: outbound bytes total
    #           item3: the detailed port information, a dictionary
    #                   {"Inbound|PORT_NUM|explaination_of_the_port":[item1, item2], "Outbound|---|NON_SERVICE_PORT":[item1, item2], ......}
    #                                                                   ^      ^
    #                                                                   |      |
    #                                                   proportion of pkts    proportion of bytes

    service_ports_dict = ut.service_port_to_dict("service-names-port-numbers.csv")
    pf_dict = ut.dict_read_from_file(file1)
    simplified_PF_dict = {}

    print("Generating simplified profiles ...")
    # enumerate the profile dictionary 
    for i, (k, v) in enumerate(pf_dict.items()):
        temp_res = [[],[],dict(),dict()]
        outbound_dict = v[0]
        inbound_dict = v[1]

        # the item3 of the simplified profile
        outbound_usage = {}
        inbound_usage = {}

        # process the outbound ports
        for j, (k_out, v_out) in enumerate(outbound_dict.items()):
            index_list = k_out.split("|")
            port = index_list[1]

            # generate the key value for port information
            if "---" in port:
                # it is a non-service port 
                port_key = "Outbound|---|NON_SERVICE_PORT"
            else:
                port_key = "Outbound|" + port + "|" + service_ports_dict[port]

            if port_key in outbound_usage:
                value_to_be_updated = [v_out[0]+outbound_dict[k_out][0], v_out[1]+outbound_dict[k_out][1]]
                outbound_usage[port_key] = value_to_be_updated 
            else:
                outbound_usage[port_key] = v_out

            if "---" in port:
                continue
            else:
                temp_res[2][port] = service_ports_dict[port]
        
        temp_res[0] = sorted(outbound_usage.items(), key=lambda item: item[1][1], reverse=True)[:num]
        
        # process the inbound ports
        for j, (k_in, v_in) in enumerate(inbound_dict.items()):
            index_list = k_in.split("|")
            port = index_list[1]

            if "-" in port:
                port_key = port
            else:
                port_key = service_ports_dict[port]

            if port_key in inbound_usage:
                value_to_be_updated = [v_in[0]+inbound_dict[k_in][0], v_in[1]+inbound_dict[k_in][1]]
                inbound_usage[port_key] = value_to_be_updated
            else:
                inbound_usage[port_key] = v_in

            if "-" in port:
                continue
            else:
                temp_res[3][port] = service_ports_dict[port]
        
        temp_res[1] = sorted(inbound_usage.items(), key=lambda item: item[1][1], reverse=True)[:num]

        simplified_PF_dict[k] = temp_res
    
    ut.dict_write_to_file(simplified_PF_dict, file2)


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

    # # # Clustering with most used service ports
    # simplified_profile_generation(5 , "profile_results.txt", "clustering_results.txt")