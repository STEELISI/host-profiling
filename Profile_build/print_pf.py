from itertools import islice
import utilities as ut
import os
import argparse
import textwrap

def print_n_profiles_v2(file,num):
    # print the first n elements in the profile dictionary

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    it = iter(pf_dict)

    for i in range(num):
        dict_key = next(it)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(dict_key) + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("========== " + "Traffic" " ==================================================================")
        for i, (k, v) in enumerate(pf_dict[dict_key].items()):
            print(k + ": " + str(v))
        print("========== " + "End" " ======================================================================")
        print()
        print()

def print_ip_profile(file,ip):
    # print the profile of IP from dictionary
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + ip + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("========== " + "Outbound Traffic" " =========================================================")
    for i, (k, v) in enumerate(pf_dict[ip][0].items()):
        print(k + ": " + str(v))
    print("========== " + "Inbound Traffic" " ================================================")
    for i, (k, v) in enumerate(pf_dict[ip][1].items()):
        print(k + ": " + str(v))
    print("========== " + "End" " ======================================================================")
    print()
    print()

def print_nth_profile(file,num):
    # print the nth element in the profile dictionary
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    it = iter(pf_dict)
    # Consume n elements.
    next(islice(it, num, num), None) 
    # Return the value at the current position.
    # This raises StopIteration if n is beyond the limits.
    # Use next(it, None) to suppress that exception.
    item = next(it)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(item) + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("========== " + "Outbound Traffic" " =========================================================")
    for i, (k, v) in enumerate(pf_dict[item][0].items()):
        print(k + ": " + str(v))
    print("========== " + "Inbound Traffic" " ================================================")
    for i, (k, v) in enumerate(pf_dict[item][1].items()):
        print(k + ": " + str(v))
    print("========== " + "End" " ======================================================================")
    print()
    print()

def print_ip_simplified_profile(file,ip):
    # print the IP in the simplified profile dictionary
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + ip + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("Topic of this IP: ")
    print(pf_dict[ip][0])
    print("========== " + "Traffic volume" " ===========================================================")
    print("Outbound total pkts: " + str(pf_dict[ip][1][0]))
    print("Outbound total bytes: " + str(pf_dict[ip][1][1]))
    print("Inbound total pkts: " + str(pf_dict[ip][1][2]))
    print("Inbound total bytes: " + str(pf_dict[ip][1][3]))
    print("========== " + "Detailed port information" " ================================================")
    for i, (k, v) in enumerate(pf_dict[ip][2].items()):
        print(k + ": " + str(v))
    print("========== " + "End" " ======================================================================")
    print()
    print()


def print_nth_simplified_profile(file,num):
    # print the nth element in the simplified profile dictionary
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    it = iter(pf_dict)
    # Consume n elements.
    next(islice(it, num, num), None) 
    # Return the value at the current position.
    # This raises StopIteration if n is beyond the limits.
    # Use next(it, None) to suppress that exception.
    item = next(it)

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(item) + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("Topic of this IP: ")
    print(pf_dict[item][0])
    print("========== " + "Traffic volume" " ===========================================================")
    print("Outbound total pkts: " + str(pf_dict[item][1][0]))
    print("Outbound total bytes: " + str(pf_dict[item][1][1]))
    print("Inbound total pkts: " + str(pf_dict[item][1][2]))
    print("Inbound total bytes: " + str(pf_dict[item][1][3]))
    print("========== " + "Detailed port information" " ================================================")
    for i, (k, v) in enumerate(pf_dict[item][2].items()):
        print(k + ": " + str(v))
    print("========== " + "End" " ======================================================================")
    print()
    print()

def print_n_profiles(file,num):
    # print the first n elements in the profile dictionary

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    it = iter(pf_dict)

    for i in range(num):
        dict_key = next(it)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(dict_key) + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("========== " + "Outbound Traffic" " =========================================================")
        for i, (k, v) in enumerate(pf_dict[dict_key][0].items()):
            print(k + ": " + str(v))
        print("========== " + "Inbound Traffic" " ================================================")
        for i, (k, v) in enumerate(pf_dict[dict_key][1].items()):
            print(k + ": " + str(v))
        print("========== " + "End" " ======================================================================")
        print()
        print()

def print_specific_item_in_dict(file, key):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    dict = ut.dict_read_from_file(filename)
    print(dict[key])


def print_n_simplified_profiles(file,num):
    # print the first n elements in the simplified profile dictionary
    
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, file)
    pf_dict = ut.dict_read_from_file(filename)

    it = iter(pf_dict)

    for i in range(num):
        dict_key = next(it)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(dict_key) + " <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("Topic of this IP: ")
        print(pf_dict[dict_key][0])
        print("========== " + "Traffic volume" " ===========================================================")
        print("Outbound total pkts: " + str(pf_dict[dict_key][1][0]))
        print("Outbound total bytes: " + str(pf_dict[dict_key][1][1]))
        print("Inbound total pkts: " + str(pf_dict[dict_key][1][2]))
        print("Inbound total bytes: " + str(pf_dict[dict_key][1][3]))
        print("========== " + "Detailed port information" " ================================================")
        for i, (k, v) in enumerate(pf_dict[dict_key][2].items()):
            print(k + ": " + str(v))
        print("========== " + "End" " ======================================================================")
        print()
        print()

if __name__ == "__main__":
    # Examples:
    #     python3 print_pf.py -spf "results/8.17_simplified_profile_results.txt" -n 20
    #     python3 print_pf.py -pf "results/8.17_profile_results.txt" -n 20
    #     python3 print_pf.py -nth_pf "results/8.17_profile_results.txt" -nth 20


    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            EXAMPLES:
                Print the first 20 simplified profiles from "results/8.17_simplified_profile_results.txt":
                    python3 print_pf.py -spf "results/8.17_simplified_profile_results.txt" -n 20
                Print the first 20 profiles from "results/8.17_profile_results.txt":
                    python3 print_pf.py -pf "results/8.17_profile_results.txt" -n 20
                Print the 20th profile from "results/8.17_profile_results.txt":
                    python3 print_pf.py -nth_pf "results/8.17_profile_results.txt" -nth 20
                Print the 20th simplified profile from "results/8.17_simplified_profile_results.txt":
                    python3 print_pf.py -nth_spf "results/8.17_simplified_profile_results.txt" -nth 20
                Print the IP address 65.89.253.157's profile from "results/8.17_profile_results.txt"
                    python3 print_pf.py -ip_pf "results/8.17_profile_results.txt" -ip "65.89.253.157"
                Print the IP address 65.89.253.157's simplified profile from "results/8.17_profile_results.txt"
                    python3 print_pf.py -ip_spf "results/8.17_simplified_profile_results.txt" -ip "65.89.253.157"
                Print the first 20 profiles (v2) from "results/8.17_profile_results_v2.txt":
                    python3 print_pf.py -pf_v2 "results/8.17_profile_results_v2.txt" -n 20
                Print IP 42.128.166.100 in dict 8.17_port_usage_for_each_endpoint.json:
                    python3 print_pf.py -dict "8.17_port_usage_for_each_endpoint.json" -ip "42.128.166.100"
        '''))
    parser.add_argument('-spf', type=str, help='The path of the simplified profile you want to print. For example: \"results/8.17_simplified_profile_results.txt\".')
    parser.add_argument('-nth_spf', type=str, help='The path of the simplified profile you want to print(the nth item). For example: \"results/8.17_simplified_profile_results.txt\".')
    parser.add_argument('-pf', type=str, help='The path of the profile you want to print. For example: \"results/8.17_profile_results.txt\".')
    parser.add_argument('-nth_pf', type=str, help='The path of the profile you want to print (the nth item). For example: \"results/8.17_profile_results.txt\".')
    parser.add_argument('-n', type=int, help='The number of items you want to print. For example: 20.')
    parser.add_argument('-nth', type=int, help='The nth item you want to print. For example: 20.')
    parser.add_argument('-ip_pf', type=str, help='The path of the profile you want to print (for an IP address). For example: \"results/8.17_profile_results.txt\".')
    parser.add_argument('-ip_spf', type=str, help='The path of the simplified profile you want to print (for an IP address). For example: \"results/8.17_simplified_profile_results.txt\".')
    parser.add_argument('-ip', type=str, help='The ip you want to print. For example: \"65.89.253.157\".')
    parser.add_argument('-pf_v2', type=str, help='The path of the profile you want to print. For example: \"results/8.17_profile_results_v2.txt\".')
    parser.add_argument('-dict', type=str, help='The path of the dictionary you want to print. For example: \"results/8.17_profile_results_v2.txt\".')
    args = parser.parse_args()

    if args.pf:
        print_n_profiles(args.pf, args.n)
    elif args.spf:
        print_n_simplified_profiles(args.spf, args.n)
    elif args.nth_pf:
        print_nth_profile(args.nth_pf, args.nth)
    elif args.nth_spf:
        print_nth_simplified_profile(args.nth_spf, args.nth)
    elif args.ip_pf:
        print_ip_profile(args.ip_pf, args.ip)
    elif args.ip_spf:
        print_ip_simplified_profile(args.ip_spf, args.ip)
    elif args.pf_v2:
        print_n_profiles_v2(args.pf_v2, args.n)
    elif args.dict:
        print_specific_item_in_dict(args.dict, args.ip)
