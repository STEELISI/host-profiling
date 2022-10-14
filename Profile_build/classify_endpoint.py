# Yebo Feng 

import argparse
import os
import utilities as ut

def is_restricted(ip):
    # return 0 if this ip is not restricted
    # return 1 if this ip is restricted
    # return 2 if this ip is invalid

    global profile_v2_dict

    # profile_dict[ip][1][IP_record_key] = ['few', {another_ip:[pkts, bytes]}]

    if ip not in profile_v2_dict:
        return 2

    for i, (k, v) in enumerate(profile_v2_dict[ip][1].items()):
        # print(v[0])
        if v[0] == 'many':
            return 0
    return 1

def has_bidirectional_traffic(ip):
    # return 0 if does not have bidirectional traffic
    # return 1 if has bidirectional traffic

    global simplified_profile_dict

    if simplified_profile_dict[ip][1][1] >= 100 and simplified_profile_dict[ip][1][3] >= 100:
        return True
    else:
        return False

def separate_ip(profile_v1_file, profile_v2_file, simplified_profile_file):

    global profile_v1_dict
    global profile_v2_dict
    global simplified_profile_dict

    # load all types of profiles 
    print("Loading all the profiles......")
    dirname = os.path.dirname(__file__)
    profile_v1_filename = os.path.join(dirname, profile_v1_file)
    profile_v1_dict = ut.dict_read_from_file(profile_v1_filename)
    profile_v2_filename = os.path.join(dirname, profile_v2_file)
    profile_v2_dict = ut.dict_read_from_file(profile_v2_filename)
    simplified_profile_filename = os.path.join(dirname, simplified_profile_file)
    simplified_profile_dict = ut.dict_read_from_file(simplified_profile_filename)

    # extract all the IP addresses as a list
    all_ip_list = list(profile_v1_dict.keys())

    # classify all the ip addresses 
    single_directional_ip_list = []
    restricted_ip_list = []
    unrestricted_ip_list = []

    for ip in all_ip_list:
        if has_bidirectional_traffic(ip):
            if is_restricted(ip) == 1:
                restricted_ip_list.append(ip)
            elif is_restricted(ip) == 0:
                unrestricted_ip_list.append(ip)
            elif is_restricted(ip) == 2:
                single_directional_ip_list.append(ip)
        else:
            single_directional_ip_list.append(ip)

    print("Invalid IP number: " + str(len(single_directional_ip_list)))
    print("Restricted IP number: " + str(len(restricted_ip_list)))
    print("Unrestricted IP number: " + str(len(unrestricted_ip_list)))
    print("Saving all the IPs......")

    ut.save_list_to_file_linebyline(single_directional_ip_list, "8.17_invalid_ip.txt")
    ut.save_list_to_file_linebyline(restricted_ip_list, "8.17_restricted_ip.txt")
    ut.save_list_to_file_linebyline(unrestricted_ip_list, "8.17_unrestricted_ip.txt")
    print("Done!")

def separate_ip_v2(profile_v2_file, simplified_profile_file):

    global profile_v2_dict
    global simplified_profile_dict

    # load all types of profiles 
    print("Loading all the profiles......")
    dirname = os.path.dirname(__file__)
    profile_v2_filename = os.path.join(dirname, profile_v2_file)
    profile_v2_dict = ut.dict_read_from_file(profile_v2_filename)
    simplified_profile_filename = os.path.join(dirname, simplified_profile_file)
    simplified_profile_dict = ut.dict_read_from_file(simplified_profile_filename)

    # extract all the IP addresses as a list
    all_ip_list = list(profile_v2_dict.keys())

    # classify all the ip addresses 
    single_directional_ip_list = []
    restricted_ip_list = []
    unrestricted_ip_list = []

    for ip in all_ip_list:
        if has_bidirectional_traffic(ip):
            if is_restricted(ip) == 1:
                restricted_ip_list.append(ip)
            elif is_restricted(ip) == 0:
                unrestricted_ip_list.append(ip)
            elif is_restricted(ip) == 2:
                single_directional_ip_list.append(ip)
        else:
            single_directional_ip_list.append(ip)

    print("Invalid IP number: " + str(len(single_directional_ip_list)))
    print("Restricted IP number: " + str(len(restricted_ip_list)))
    print("Unrestricted IP number: " + str(len(unrestricted_ip_list)))
    print("Saving all the IPs......")

    ut.save_list_to_file_linebyline(single_directional_ip_list, "8.19_invalid_ip_v2.txt")
    ut.save_list_to_file_linebyline(restricted_ip_list, "8.19_restricted_v2.txt")
    ut.save_list_to_file_linebyline(unrestricted_ip_list, "8.19_unrestricted_v2.txt")
    print("Done!")

if __name__ == "__main__":
    # python3 classify_endpoint.py -p_v1 "results/8.17_profile_results.txt" -p_v2 "results/8.17_profile_results_v2.json" -p_sf "results/8.17_simplified_profile_results.txt"
    # python3 classify_endpoint.py -p_v2 "results/8.17_profile_results_v2.json" -p_sf "results/8.17_simplified_profile_results_v2.json"

    parser = argparse.ArgumentParser()
    parser.add_argument('-p_v1', type=str, help='The path of profile (v1). For example: \"results/8.17_profile_results.txt\".')
    parser.add_argument('-p_v2', type=str, help='The path of profile (v2). For example: \"results/8.17_profile_results_v2.json\".')
    parser.add_argument('-p_sf', type=str, help='The path of profile (simplified). For example: \"results/8.17_simplified_profile_results.txt\".')
    args = parser.parse_args()

    if args.p_v1:
        separate_ip(args.p_v1, args.p_v2, args.p_sf)
    elif args.p_v2:
        separate_ip_v2(args.p_v2, args.p_sf)